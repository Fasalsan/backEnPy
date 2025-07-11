from fastapi import FastAPI
from routes import product_routes, category_routes, customer_routes,sale_routes

app = FastAPI()

app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])
app.include_router(customer_routes.router, prefix="/customer", tags=["Customers"])
app.include_router(sale_routes.router, prefix="/saleOrder", tags=["SaleOrder"])
