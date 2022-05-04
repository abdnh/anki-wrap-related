import re
from typing import List, Tuple

from anki.notes import Note

try:
    from anki.utils import strip_html
except:
    from anki.utils import stripHTML as strip_html

CLOZE_RE = re.compile(f"(?si)\[\[c(\d+)::.*?\]\]")


def get_current_cloze_number(note: Note) -> int:
    text = " ".join(note.values())
    text = strip_html(text)
    try:
        n = max(int(m.group(1)) for m in CLOZE_RE.finditer(text))
        return n
    except:
        return 0


def wrap_in_cloze(note: Note, contents: str, n: int) -> Tuple[int, str]:
    if not n:
        n = get_current_cloze_number(note) + 1
    return n, f"{{{{c{n}::{contents}}}}}"


class WrapOp:
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
        n, replaced = wrap_in_cloze(note, phrase, self.current_cloze)
        if self.repeat:
            self.current_cloze = n
        else:
            self.current_cloze = n + 1
        return replaced


def wrap_related(
    note: Note, search_field: str, highlight_field: str, wrap_ops: List[WrapOp]
) -> str:
    if search_field not in note or highlight_field not in note:
        return ""
    search = strip_html(note[search_field])
    highlight_field_contents = note[highlight_field]

    pattern = re.compile(f"{re.escape(search)}")
    for wrap_op in wrap_ops:
        highlight_field_contents = pattern.sub(
            lambda m: wrap_op.handle(note, m.group(0)),
            highlight_field_contents,
        )

    return highlight_field_contents
