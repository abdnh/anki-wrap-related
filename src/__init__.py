from typing import List

import aqt
from aqt.browser.browser import Browser
from aqt.editor import Editor
from aqt.gui_hooks import browser_menus_did_init, editor_did_init_buttons
from aqt.operations import CollectionOp
from aqt.qt import *
from aqt.utils import tooltip

from . import consts
from .dialog import WrapRelatedDialog


def on_bulk_updated_notes(browser: Browser, updated_count: int) -> None:
    if updated_count:
        tooltip(f"Updated {updated_count} note(s).", parent=browser)


def on_browser_action_triggered(browser: Browser) -> None:
    notes = [browser.mw.col.get_note(nid) for nid in browser.selected_notes()]
    dialog = WrapRelatedDialog(browser.mw, browser, notes)
    if dialog.exec():
        updated_notes = dialog.updated_notes
        CollectionOp(
            parent=browser,
            op=lambda col: col.update_notes(updated_notes),
        ).success(
            lambda out: on_bulk_updated_notes(browser, len(updated_notes)),
        ).run_in_background()


def on_browser_menus_did_init(browser: Browser) -> None:
    config = aqt.mw.addonManager.getConfig(__name__)
    action = QAction(consts.ADDON_NAME, browser)
    action.setShortcut(config["browser_shortcut"])
    qconnect(action.triggered, lambda: on_browser_action_triggered(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(action)


def on_editor_button_clicked(editor: Editor) -> None:
    dialog = WrapRelatedDialog(editor.mw, editor.parentWindow, [editor.note])
    if dialog.exec():
        editor.loadNoteKeepingFocus()


def on_editor_did_init_buttons(buttons: List[str], editor: Editor) -> None:
    config = aqt.mw.addonManager.getConfig(__name__)
    shortcut = config["editor_shortcut"]
    button = editor.addButton(
        icon=os.path.join(consts.ICONS_DIR, "box-arrow-in-down.svg"),
        cmd=consts.ADDON_PACKAGE,
        tip=f"{consts.ADDON_NAME} ({shortcut})" if shortcut else consts.ADDON_NAME,
        func=on_editor_button_clicked,
        keys=shortcut,
    )
    buttons.append(button)


browser_menus_did_init.append(on_browser_menus_did_init)
editor_did_init_buttons.append(on_editor_did_init_buttons)
