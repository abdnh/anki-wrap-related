import re
from typing import List, Tuple

from anki.notes import Note

try:
    from anki.utils import strip_html
except ImportError:
    from anki.utils import stripHTML as strip_html

CLOZE_RE = re.compile(r"(?si)\[\[c(\d+)::.*?\]\]")


def get_current_cloze_number(note: Note) -> int:
    text = " ".join(note.values())
    text = strip_html(text)
    try:
        num = max(int(m.group(1)) for m in CLOZE_RE.finditer(text))
        return num
    except:
        return 0


def wrap_in_cloze(note: Note, contents: str, num: int) -> Tuple[int, str]:
    if not num:
        num = get_current_cloze_number(note) + 1
    return num, f"{{{{c{num}::{contents}}}}}"


class WrapOp:
    # Whether this operation works by finding & replacing patterns from the search field in the highlight field.
    by_pattern: bool = True

    def handle(self, note: Note, phrase: str) -> str:
        return phrase


class HighlighOp(WrapOp):
    def __init__(self, color: str = "#0000ff"):
        self.color = color

    def handle(self, note: Note, phrase: str) -> str:
        return f'<span style="color: {self.color};">{phrase}</span>'


class ClozeOp(WrapOp):
    def __init__(self, repeat: bool = True):
        self.repeat = repeat
        self.current_cloze = 0

    def handle(self, note: Note, phrase: str) -> str:
        # TODO: if the phrase is wrapped in clozes, maybe remove them before clozing again?
        num, replaced = wrap_in_cloze(note, phrase, self.current_cloze)
        if self.repeat:
            self.current_cloze = num
        else:
            self.current_cloze = num + 1
        return replaced


class ClozeHintOp(WrapOp):
    by_pattern = False

    def __init__(self, char_count: int):
        self.char_count = char_count

    def handle(self, note: Note, phrase: str) -> str:
        phrase = strip_html(phrase)
        replaced = ""
        for word in phrase.split():
            word = (
                word[: self.char_count]
                + wrap_in_cloze(note, word[self.char_count :], 0)[1]
            )
            replaced += f"{word} "
        return replaced


def wrap_related(
    note: Note,
    search_field: str,
    highlight_field: str,
    wrap_ops: List[WrapOp],
    separate_phrases: bool,
) -> str:
    if search_field not in note or highlight_field not in note:
        return ""
    search = strip_html(note[search_field])
    parts = []
    if separate_phrases:
        parts = search.split("*")
    else:
        parts = [search]
    pattern = re.compile("|".join(re.escape(part) for part in parts))
    highlight_field_contents = note[highlight_field]
    for wrap_op in wrap_ops:
        if wrap_op.by_pattern:
            highlight_field_contents = pattern.sub(
                lambda m: wrap_op.handle(  # pylint: disable=cell-var-from-loop
                    note, m.group(0)
                ),
                highlight_field_contents,
            )
        else:
            highlight_field_contents = wrap_op.handle(note, highlight_field_contents)

    return highlight_field_contents
