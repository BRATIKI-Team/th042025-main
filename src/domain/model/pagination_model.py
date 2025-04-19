from typing import Generic, TypeVar


T = TypeVar("T")


class PaginationModel(Generic[T]):
    def __init__(self, page: int, page_size: int, items: list[T], has_more: bool):
        self._page = page
        self._page_size = page_size
        self._items = items
        self._has_more = has_more

    @property
    def page(self) -> int:
        return self._page

    @property
    def page_size(self) -> int:
        return self._page_size

    @property
    def items(self) -> list[T]:
        return self._items

    @property
    def has_more(self) -> bool:
        return self._has_more
