from typing import List, Any, Type, Generic, TypeVar, Optional
from urllib.parse import parse_qsl, urlencode

from fastapi import Request
from loguru import logger
from pydantic import BaseModel

from src.seedwork.infra.schemas.pagination import (
    PageMeta,
    PageLink,
    PageResult,
)

T = TypeVar("T", bound=BaseModel)


class Pagination(Generic[T]):
    """
    Classe para criar objetos de paginação em respostas de APIs.

    Esta classe permite gerar uma estrutura de paginação consistente para ser utilizada nas respostas das APIs,
    suportando tanto a paginação realizada no banco de dados quanto a paginação realizada em código.

    Parâmetros:
    - request (Request): Objeto de requisição do FastAPI.
    - items (List[Any]): Lista de itens a serem incluídos na página atual.
    - page (int): Número da página atual.
    - page_size (int): Número de itens por página.
    - schema_class (Type[T]): Classe Pydantic utilizada para serializar os itens.
    - total_items (Optional[int]): Total de itens disponíveis. Se não for fornecido, será calculado com base no tamanho da lista `items`.
    - paginate_in_code (bool): Indica se a paginação deve ser realizada em código (True) ou se os itens já estão paginados (False).

    Funcionamento:

    Paginação no Banco de Dados (paginate_in_code=False):
    Quando a paginação é realizada diretamente na consulta ao banco de dados, os itens fornecidos em `items`
    já correspondem à página solicitada. Neste caso, é necessário informar o total de itens disponíveis em `total_items`
    para que o cálculo de `total_pages` seja correto. A classe utiliza `total_items` para gerar os metadados e links de paginação.

    Paginação em Código (paginate_in_code=True):
    Quando todos os itens são recuperados do banco de dados sem paginação, a classe realiza a paginação em código.
    Os itens são fatiados internamente com base nos parâmetros `page` e `page_size`. O total de itens é calculado
    automaticamente usando `len(items)`, caso `total_items` não seja fornecido.


    Exemplo de Uso:

    Paginação no Banco de Dados:
    total_items = use_case.count_all(db)
    offset = (page - 1) * page_size
    limit = page_size
    items = use_case.get_all(db, offset=offset, limit=limit)
    result = Pagination[ItemSchema].create(
        request=request,
        items=items,
        total_items=total_items,
        page=page,
        page_size=page_size,
        schema_class=ItemSchema,
    )

    Paginação em Código:
    items = use_case.get_all(db)
    result = Pagination[ItemSchema].create(
        request=request,
        items=items,
        page=page,
        page_size=page_size,
        schema_class=ItemSchema,
        paginate_in_code=True,
    )

    Observação:
    A escolha entre paginação no banco de dados ou em código depende do contexto e das necessidades de performance da aplicação.
    Para conjuntos de dados grandes, é recomendado realizar a paginação no banco de dados para reduzir o consumo de memória
    e o tempo de processamento. A classe Pagination foi projetada para acomodar ambas as abordagens de forma transparente.
    """

    @classmethod
    def create(
        cls,
        *,
        request: Request,
        items: List[Any],
        page: int,
        page_size: int,
        schema_class: Type[T],
        total_items: Optional[int] = None,
        paginate_in_code: bool = False,
    ) -> PageResult[T]:
        if total_items is None:
            logger.debug("user_ids deve ser uma lista.")
            total_items = len(items)

        total_pages = max(1, (total_items + page_size - 1) // page_size)

        if page > total_pages:
            paginated_items = []
        else:
            if paginate_in_code:
                start_index = (page - 1) * page_size
                end_index = start_index + page_size
                paginated_items = items[start_index:end_index]
            else:
                paginated_items = items

        pydantic_items = [
            schema_class.model_validate(item) for item in paginated_items
        ]

        actual_page = str(request.url)
        base_url, _, query_string = actual_page.partition("?")
        existing_params = dict(parse_qsl(query_string))
        existing_params["page_size"] = str(page_size)

        def build_url(new_page: int) -> str:
            params = existing_params.copy()
            params["page"] = str(new_page)
            return f"{base_url}?{urlencode(params)}"

        next_page = build_url(page + 1) if page < total_pages else None
        prev_page = build_url(page - 1) if page > 1 else None

        return PageResult[T](
            items=pydantic_items,
            meta=PageMeta(
                page=page,
                page_size=page_size,
                total_items=total_items,
                total_pages=total_pages,
            ),
            links=PageLink(
                next_page=next_page,
                prev_page=prev_page,
                actual_page=actual_page,
            ),
        )
