from fastapi import FastAPI
from routes import product_routes, category_routes

app = FastAPI()

app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])
