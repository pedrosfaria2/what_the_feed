from src.seedwork.infra.schemas import GetInput
from src.seedwork.infra.schemas.pagination import PageResult
from src.seedwork.infra.schemas import PydanticModel


class GetGenericInput(GetInput):
    pass


class GetGenericOutput(PageResult):
    pass


class DeleteGenericOutput(PydanticModel):
    status: str
    metadata: dict
