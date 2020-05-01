from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

from src.discord_parser import *
import pathlib
from pathlib import *
from typing import *


class DocBuilder():
    # Value of the constant defines processing priority
    F_MARGIN = -1
    F_TITLE = 0
    F_AUTHOR = 1
    F_DATE = 2
    F_INDEX = 3

    def __init__(self):
        super().__init__()
        self.__preamble = dict()
        self.__features = dict()
        self.__geometry = dict()
        self.__callback = {
            DocBuilder.F_TITLE: self.__make_title,
            DocBuilder.F_AUTHOR: self.__make_author,
            DocBuilder.F_DATE: self.__make_date,
            DocBuilder.F_INDEX: self.__make_index
        }

    def set_margin(self, margin: float):
        self.__geometry[DocBuilder.F_MARGIN] = margin
        return self

    def set_title(self, title: str):
        self.__preamble[DocBuilder.F_TITLE] = title
        return self

    def set_author(self, author: str):
        self.__preamble[DocBuilder.F_AUTHOR] = author
        return self

    def set_date(self, date: str = r"\today"):
        self.__preamble[DocBuilder.F_DATE] = date
        return self

    def add_index(self, label="Contents"):
        self.__features[DocBuilder.F_INDEX] = label
        return self

    def reset(self):
        self.__geometry = dict()
        self.__features = dict()
        self.__preamble = dict()
        return self

    def build(self) -> Document():
        return self.__make_document()

    def __make_document(self) -> Document:
        geom = self.__make_geometry()
        doc = Document(geometry_options=geom) if geom else Document()
        doc = self.__make_preamble(doc)
        doc = self.__make_features(doc)
        return doc

    def __make_geometry(self) -> dict:
        geom = dict()
        if DocBuilder.F_MARGIN in self.__geometry.keys():
            geom["margin"] = "{}in".format(self.__geometry[DocBuilder.F_MARGIN])
        return geom

    def __make_preamble(self, doc : Document) -> Document:
        for p in sorted(self.__preamble.keys()):
            doc = self.__callback[p](doc)
        doc.append(NoEscape(r"\maketitle"))
        doc.append(NoEscape(r"\newpage"))
        return doc

    def __make_features(self, doc : Document) -> Document:
        for f in sorted(self.__features.keys()):
            doc = self.__callback[f](doc)
        return doc

    def __make_title(self, doc: Document) -> Document:
        doc.preamble.append(Command("title", self.__preamble[DocBuilder.F_TITLE]))
        return doc

    def __make_author(self, doc: Document) -> Document:
        doc.preamble.append(Command("author", self.__preamble[DocBuilder.F_AUTHOR]))
        return doc

    def __make_date(self, doc: Document) -> Document:
        doc.preamble.append(Command("date", NoEscape(self.__preamble[DocBuilder.F_DATE])))
        return doc

    def __make_index(self, doc: Document) -> Document:
        doc.append(NoEscape(r"\renewcommand{{\contentsname}}{{{}}}\tableofcontents\newpage".format(
            self.__features[DocBuilder.F_INDEX]
        )))
        return doc


class DocMaker():

    def __init__(self):
        super().__init__()
        self.__features = dict()

    def makedoc(self, data: dict, title: str, author: str, date=None) -> Document:
        doc = DocBuilder().set_margin(1).set_title(title).set_author(author).set_date().add_index("Indice").build()
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
