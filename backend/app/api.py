from fastapi import APIRouter
from app.modules.evoucher.router import router as evoucher_router
from app.modules.academics.router import router as academics_router

api_router = APIRouter()

api_router.include_router(evoucher_router, prefix="/evoucher", tags=["evoucher"])
api_router.include_router(academics_router, prefix="/academics", tags=["academics"])
