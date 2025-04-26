from typing import List, Optional, TypeVar, Generic
from src.seedwork.infra.schemas import PydanticModel, Field
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PageMeta(PydanticModel):
    page: int = Field(description="Página atual")
    page_size: int = Field(description="Items solicitados por página")
    total_items: int = Field(description="Total de itens que podem ser consultados")
    total_pages: int = Field(
        description="Total de páginas gerado pelo total de itens dividido pelo itens solicitados"
    )


class PageLink(PydanticModel):
    next_page: Optional[str] = Field(description="Next Page to be queried")
    prev_page: Optional[str] = Field(
        description="Previous page, if any, that was queried"
    )
    actual_page: str = Field(description="The actual page url that was queried")


class PageResult(PydanticModel, Generic[T]):
    items: List[T]
    links: PageLink
    meta: PageMeta
