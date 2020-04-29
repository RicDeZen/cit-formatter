import json
import re
from pathlib import Path


class ChatMessage():
    '''
    Class defining a Chat message. Subclasses define what info is actually parsed.
    '''

    def __init__(self, content, author):
        super().__init__()
        self.__content = content
        self.__author = author

    def get_content(self):
        return self.__content

    def get_author(self):
        return self.__author

    def __repr__(self):
        return "ChatMessage: {}".format({self.__author, self.__content})


class QuoteMessage(ChatMessage):
    '''
    Class defining a message that contains a quote.
    The author is not the one who wrote the message,
    but the person who originally said the quote.
    '''

    def __init__(self, quote, author):
        super().__init__(quote, author)


class ChatParser():

    def __init__(self):
        super().__init__()
        self.__message

    def can_parse(self, d: dict) -> bool:
        return "messages" in d.keys()

    def parse(self, d: dict) -> list:
        messages = self.get_list(d)
        chat_msg = [self.get_msg(m) for m in messages]
        return [m for m in chat_msg if m] if chat_msg else list()

    def get_list(self, d: dict) -> list:
        if "messages" not in d.keys() : return list()
        return list(d["messages"])

    def get_msg(self, m: dict) -> ChatMessage:
        if "content" not in m.keys() : return None
        if "author" not in m.keys() : return None
        if type(m["author"]) != dict or "name" not in m["author"].keys() : return None
        return ChatMessage(m["content"], m["author"]["name"])


class QuoteParser(ChatParser):
    def __init__(self):
        super().__init__()

    def can_parse(self, d: dict) -> bool:
        return "messages" in d.keys()

    def parse(self, d: dict) -> list:
        messages = self.get_list(d)
        quote_msg = [self.get_quote(m) for m in messages]
        return [m for m in quote_msg if m] if quote_msg else list()

    def get_list(self, d: dict) -> list:
        if "messages" not in d.keys() : return list()
        return list(d["messages"])

    def get_quote(self, m: dict) -> QuoteMessage:
        p = re.search("(?P<quote>(> .+\\n)+)@(?P<author>.+)", m["content"])
        return QuoteMessage(p.group("quote"), p.group("author")) if p else None