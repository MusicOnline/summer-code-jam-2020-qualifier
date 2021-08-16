"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import string
import typing

T = typing.TypeVar("T", bound=typing.Type[typing.Any])


class ArticleField(typing.Generic[T]):
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: T) -> None:
        self.field_type: T = field_type

    def __set_name__(self, owner: typing.Any, name: str) -> None:
        self.name: str = name

    def __set__(self, instance: typing.Any, value: typing.Any) -> None:
        if isinstance(value, self.field_type):
            instance.__dict__[self.name] = value
        else:
            raise TypeError(
                f"expected an instance of type {self.field_type.__name__!r} "
                f"for attribute {self.name!r}, got {type(value).__name__!r} instead"
            )

    def __get__(self, instance: typing.Any, owner: typing.Any = None) -> typing.Any:
        return instance.__dict__[self.name]


class Article:
    """The `Article` class you need to write for the qualifier."""

    count: int = 0
    id = ArticleField(int)
    title = ArticleField(str)
    author = ArticleField(str)
    _content = ArticleField(str)
    publication_date = ArticleField(datetime.datetime)

    def __init__(
        self, title: str, author: str, publication_date: datetime.datetime, content: str
    ) -> None:
        self.id = Article.count
        Article.count += 1
        self.title = title
        self.author = author
        self._content = content
        self.publication_date = publication_date
        self.last_edited: typing.Optional[datetime.datetime] = None

    def __repr__(self) -> str:
        return (
            "<Article title={0.title!r} author={0.author!r} publication_date={publication_date!r}>"
        ).format(self, publication_date=self.publication_date.isoformat())

    def __len__(self) -> int:
        return len(self.content)

    def __gt__(self, other: "Article") -> bool:
        # To allow sort comparisons
        return self.publication_date.__gt__(other.publication_date)

    def short_introduction(self, n_characters: int) -> str:
        # Assume positive integers only
        if len(self.content) <= n_characters:
            return self.content
        for negative_index, character in enumerate(
            reversed(self.content[: n_characters + 1]), 1
        ):
            if character in [" ", "\n"]:
                return self.content[: n_characters + 1][:-negative_index]
        assert False, "Something unexpected happened and mypy wants me to handle it"

    def most_common_words(self, n_words: int) -> typing.Dict[str, int]:
        lowered_string: str = self.content.lower()
        words: typing.Dict[str, int] = {}
        current_word_first_index: int = -1
        word: str
        # -1 means this iteration is not within a word yet

        def _add_word(word):
            if word not in words:
                words[word] = 1
            else:
                words[word] += 1

        for index, character in enumerate(lowered_string):
            if (
                character not in string.ascii_lowercase
                and current_word_first_index != -1
            ):
                word = lowered_string[current_word_first_index:index]
                _add_word(word)
                current_word_first_index = -1
            if character in string.ascii_lowercase and current_word_first_index == -1:
                current_word_first_index = index

        # Handle last word if string does not end with a non-alphabet character
        if current_word_first_index != -1:
            word = lowered_string[current_word_first_index:]
            _add_word(word)

        return {
            word: frequency
            for word, frequency in sorted(
                words.items(), key=lambda item: item[1], reverse=True
            )[:n_words]
        }

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self._content = value
        self.last_edited = datetime.datetime.now()
