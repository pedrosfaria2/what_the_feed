import sys
from typing import List, Optional, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request, status, HTTPException
from loguru import logger
from src.seedwork.app.base import (
    GetOneService,
    GetManyService,
    PostService,
    PutService,
    DeleteService,
)
from src.seedwork.infra.defaults.base import Base
from src.seedwork.infra.repository.base import (
    GetOneRepository,
    GetManyRepository,
    PostRepository,
    PutRepository,
    DeleteRepository,
)

# from infra.common.logging import LogAPIRoute
from src.seedwork.infra.schemas.base import (
    GetGenericInput,
    GetGenericOutput,
    DeleteGenericOutput,
)


class GenericApi(APIRouter):
    """
    Define a generic API router with logging and authentication requirements.

    This class initializes a router that logs all requests and enforces authentication for each request.

    Args:
        custom_dependencies: list of additional dependencies besides authentication
    """

    def __init__(self, custom_dependencies: Optional[List[Depends]] = None):
        try:
            dependencies = []
            if custom_dependencies:
                dependencies += custom_dependencies
            super().__init__(dependencies=dependencies)
        except Exception as error:
            logger.error(f"Error during APIRouter initialization: {error}")


class GetApi:
    async def get_many_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: GetGenericOutput,
        input_params: GetGenericInput = Depends(),
    ) -> BaseModel:
        try:
            url = request.url
            input_params._actual_page = f"{url.path}?{url.query}"
            usecase = GetManyService(
                GetManyRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output
        except Exception as exp:
            detail = f"Get API error {str(exp)}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    async def get_one_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: BaseModel,
        input_params: BaseModel = Depends(),
    ) -> BaseModel:
        try:
            usecase = GetOneService(
                GetOneRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output
        except Exception as exp:
            detail = f"Get API error {str(exp)}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )


class PostApi:
    async def post_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: BaseModel,
        input_params: BaseModel,
    ):
        try:
            usecase = PostService(
                PostRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output.model_dump()
        except Exception as exp:
            detail = f"Post API error {str(exp)}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )


class PutApi:
    async def put_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: BaseModel,
        input_params: BaseModel,
    ):
        try:
            usecase = PutService(
                PutRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output.model_dump()
        except Exception as exp:
            detail = f"Post API error {str(exp)}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )


class DeleteApi:
    async def delete_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: DeleteGenericOutput,
        input_params: BaseModel = Depends(),
    ):
        try:
            usecase = DeleteService(
                DeleteRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output.model_dump()
        except Exception as exp:
            detail = f"Post API error {str(exp)}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )
