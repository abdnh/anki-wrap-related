from concurrent.futures import Future
from typing import List, Optional

from anki.notes import Note
from aqt import qtmajor
from aqt.main import AnkiQt
from aqt.qt import *
from aqt.utils import showWarning

from . import consts
from .wrap import ClozeOp, HighlighOp, WrapOp, wrap_related

if qtmajor > 5:
    from .forms.form_qt6 import Ui_Dialog
else:
    from .forms.form_qt5 import Ui_Dialog  # type: ignore

PROGRESS_LABEL = "Processed {count} out of {total} note(s)"


class WrapRelatedDialog(QDialog):
    def __init__(self, mw: AnkiQt, parent: QWidget, notes: List[Note]):
        super().__init__(parent)
        self.mw = mw
        self.config = mw.addonManager.getConfig(__name__)
        self.notes = notes
        self.updated_notes: List[Note] = []
        self.setup_ui()

    def setup_ui(self) -> None:
        self.form = Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(consts.ADDON_NAME)
        qconnect(self.form.processButton.clicked, self.on_process)
        qconnect(
            self.form.clozeCheckbox.toggled,
            self.form.increasingClozeCheckbox.setEnabled,
        )
        self.fields: List[str] = []
        for note in self.notes:
            for field in note.keys():
                if field not in self.fields:
                    self.fields.append(field)
        self.form.searchFieldComboBox.addItems(self.fields)
        self.form.highlightFieldComboBox.addItems(self.fields)

    def exec(self) -> int:
        mids = set(note.mid for note in self.notes)
        if len(mids) > 1:
            showWarning(
                "Please select notes from only one notetype.",
                parent=self,
                title=consts.ADDON_NAME,
            )
            return 0

        search_field = self.config["search_field"]
        if search_field := self._get_field(self.fields, search_field):
            self.form.searchFieldComboBox.setCurrentText(search_field)

        highlight_field = self.config["highlight_field"]
        if highlight_field := self._get_field(self.fields, highlight_field):
            self.form.highlightFieldComboBox.setCurrentText(highlight_field)
        else:
            self.form.highlightFieldComboBox.setCurrentIndex(1)
        highlight = self.config["highlight"]
        self.form.highlightCheckBox.setChecked(highlight)
        cloze = self.config["cloze"]
        self.form.clozeCheckbox.setChecked(cloze)
        increasing_cloze = self.config["increasing_cloze"]
        self.form.increasingClozeCheckbox.setChecked(increasing_cloze)
        self.form.increasingClozeCheckbox.setEnabled(cloze)
        glob_search = self.config["glob_search"]
        self.form.globCheckBox.setChecked(glob_search)

        return super().exec()

    def _get_field(self, fields: List[str], key: str) -> Optional[str]:
        for field in fields:
            if key.lower() == field.lower():
                return field
        return None

    def _process_notes(
        self,
        search_field: str,
        highlight_field: str,
        highlight: bool,
        cloze: bool,
        increasing_cloze: bool,
        glob_search: bool,
    ) -> None:
        self.updated_notes = []
        for i, note in enumerate(self.notes):
            if i % 20 == 0:
                self.mw.taskman.run_on_main(
                    lambda i=i: self.mw.progress.update(
                        label=PROGRESS_LABEL.format(count=i, total=len(self.notes)),
                        value=i + 1,
                        max=len(self.notes),
                    )
                )
            wrap_ops: List[WrapOp] = []
            if cloze:
                if increasing_cloze:
                    wrap_ops.append(ClozeOp(repeat=False))
                else:
                    wrap_ops.append(ClozeOp(repeat=True))
            if highlight:
                # TODO: make color customizable
                wrap_ops.append(HighlighOp())
            copied = wrap_related(
                note, search_field, highlight_field, wrap_ops, glob_search
            )
            if copied:
                note[highlight_field] = copied
                self.updated_notes.append(note)

    def on_process(self) -> None:
        search_field = self.fields[self.form.searchFieldComboBox.currentIndex()]
        highlight_field = self.fields[self.form.highlightFieldComboBox.currentIndex()]
        highlight = self.form.highlightCheckBox.isChecked()
        cloze = self.form.clozeCheckbox.isChecked()
        increasing_cloze = self.form.increasingClozeCheckbox.isChecked()
        glob_search = self.form.globCheckBox.isChecked()

        # save options
        self.config["search_field"] = search_field
        self.config["highlight_field"] = highlight_field
        self.config["highlight"] = highlight
        self.config["cloze"] = cloze
        self.config["increasing_cloze"] = increasing_cloze
        self.config["glob_search"] = glob_search
        self.mw.addonManager.writeConfig(__name__, self.config)

        def on_done(fut: Future) -> None:
            try:
                fut.result()
            finally:
                self.mw.taskman.run_on_main(self.mw.progress.finish)
            self.accept()

        self.mw.progress.start(
            max=len(self.notes),
            label=PROGRESS_LABEL.format(count=0, total=len(self.notes)),
            parent=self,
        )
        self.mw.progress.set_title(consts.ADDON_NAME)
        self.mw.taskman.run_in_background(
            lambda: self._process_notes(
                search_field,
                highlight_field,
                highlight,
                cloze,
                increasing_cloze,
                glob_search,
            ),
            on_done=on_done,
        )
