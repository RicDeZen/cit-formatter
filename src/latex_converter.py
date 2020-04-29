from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

from src.discord_parser import *
import pathlib
from pathlib import *
from typing import *


class DocBuilder():

    def __init__(self):
        super().__init__()
        self.__features = dict()

    def makedoc(self, data: dict, title: str, author: str, date=None) -> Document:
        doc = get_template_doc(title=title, author=author, index=True, date=date)
        doc = add_quote_section(
            doc, data, lambda l: list_formatter(l, basic_quote_formatter)
        )
        return doc


def get_template_doc(*, title: str, author: str, index=False, date=None) -> Document:
    doc = Document(geometry_options={"margin": "1in"})
    doc.preamble.append(Command("title", title))
    doc.preamble.append(Command("author", author))
    doc.preamble.append(Command("date", NoEscape(date if date else r"\today")))
    doc.append(NoEscape(r"\maketitle"))
    doc.append(NoEscape(r"\newpage"))
    if index:
        doc.append(NoEscape(r"\tableofcontents\newpage"))
    return doc


def add_quote_section(doc: Document, subsections: dict, content_formatter: Callable) -> Document:
    with doc.create(Section("Quotes")):
        for s, c in subsections.items():
            with doc.create(Subsection(s)):
                doc.append(NoEscape(content_formatter(c)))
                doc.append(NoEscape(r"\newline"))
    return doc


def list_formatter(stuff: list, item_formatter: Callable) -> str:
    return "\\newline".join([NoEscape(item_formatter(x)) for x in stuff])


def basic_quote_formatter(quote: QuoteMessage) -> str:
    return r"\emph{{{}}}\newline- {}".format(quote.get_content(), quote.get_author())


def group_msg_by_author(msg_list: list) -> dict:
    authors = set([m.get_author() for m in msg_list])
    return {a: [m for m in msg_list if m.get_author() == a] for a in authors}
