from typing import Optional, Union

from fastapi import APIRouter, Depends, Query, Path
from starlette import status
from starlette.responses import JSONResponse

from src.api.v1.dto import ProductDTO
from src.api.v1.dependencies.database import ProductRepositoryDependencyMarker
from src.api.v1.dependencies.services import SecurityGuardServiceDependencyMarker
from src.services.database.models.product import Product as _DB_Product
from src.services.database.repositories.product_repository import ProductRepository
from src.utils.responses import get_pydantic_model_or_return_raw_response

api_router = APIRouter(dependencies=[Depends(SecurityGuardServiceDependencyMarker)])


@api_router.get(
    "/products/get/{product_id}",
    responses={200: {"model": ProductDTO}}
)
async def get_product_by_id(
        product_id: int = Path(...),
        product_repository: ProductRepository = Depends(ProductRepositoryDependencyMarker),
) -> Union[JSONResponse, ProductDTO]:
    product: _DB_Product = await product_repository.get_product_by_id(product_id)
    return get_pydantic_model_or_return_raw_response(ProductDTO, product)


@api_router.get("/test_api/{user_id}/items/{item_id}", status_code=status.HTTP_200_OK,
                include_in_schema=False)
async def read_user_item(
        user_id: int,
        item_id: str,
        short: bool = False,
        q: Optional[str] = Query(None, max_length=50, deprecated=True),
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
