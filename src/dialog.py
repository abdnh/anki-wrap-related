from concurrent.futures import Future
from typing import List, Optional, Sequence

from aqt.qt import *
from aqt import qtmajor
from aqt.main import AnkiQt
from anki.notes import Note
from aqt.utils import showWarning

if qtmajor > 5:
    from .form_qt6 import Ui_Dialog
else:
    from .form_qt5 import Ui_Dialog  # type: ignore
from . import consts
from .wrap import WrapOp, wrap_related, HighlighOp, ClozeOp

PROGRESS_LABEL = "Processed {count} out of {total} note(s)"


class WrapRelatedDialog(QDialog):
    def __init__(self, mw: AnkiQt, parent, notes: List[Note]):
        super().__init__(parent)
        self.mw = mw
        self.config = mw.addonManager.getConfig(__name__)
        self.notes = notes
        self.setup_ui()

    def setup_ui(self):
        self.form = Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(consts.ADDON_NAME)
        qconnect(self.form.processButton.clicked, self.on_process)
        qconnect(
            self.form.clozeCheckbox.toggled,
            lambda checked: self.form.increasingClozeCheckbox.setEnabled(checked),
        )
        self.fields = []
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

        return super().exec()

    def _get_field(self, fields: List[str], key) -> Optional[str]:
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
    ):
        self.updated_notes = []
        for i, note in enumerate(self.notes):
            if i % 20 == 0:
                self.mw.taskman.run_on_main(
                    lambda: self.mw.progress.update(
                        label=PROGRESS_LABEL.format(count=i, total=len(self.notes)),
                        value=i + 1,
                        max=len(self.notes),
                    )
                )
            wrap_ops: Sequence[WrapOp] = []
            if cloze:
                if increasing_cloze:
                    wrap_ops.append(ClozeOp(repeat=False))
                else:
                    wrap_ops.append(ClozeOp(repeat=True))
            if highlight:
                # TODO: make color customizable
                wrap_ops.append(HighlighOp())
            copied = wrap_related(note, search_field, highlight_field, wrap_ops)
            if copied:
                note[highlight_field] = copied
                self.updated_notes.append(note)

    def on_process(self):
        search_field = self.fields[self.form.searchFieldComboBox.currentIndex()]
        highlight_field = self.fields[self.form.highlightFieldComboBox.currentIndex()]
        highlight = self.form.highlightCheckBox.isChecked()
        cloze = self.form.clozeCheckbox.isChecked()
        increasing_cloze = self.form.increasingClozeCheckbox.isChecked()

        # save options
        self.config["search_field"] = search_field
        self.config["highlight_field"] = highlight_field
        self.config["highlight"] = highlight
        self.config["cloze"] = cloze
        self.config["increasing_cloze"] = increasing_cloze
        self.mw.addonManager.writeConfig(__name__, self.config)

        def on_done(fut: Future):
            try:
                fut.result()
            finally:
                self.mw.taskman.run_on_main(lambda: self.mw.progress.finish())
            self.accept()

        self.mw.progress.start(
            max=len(self.notes),
            label=PROGRESS_LABEL.format(count=0, total=len(self.notes)),
            parent=self,
        )
        self.mw.progress.set_title(consts.ADDON_NAME)
        self.mw.taskman.run_in_background(
            lambda: self._process_notes(
                search_field, highlight_field, highlight, cloze, increasing_cloze
            ),
            on_done=on_done,
        )
