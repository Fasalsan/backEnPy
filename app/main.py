from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import product_routes, category_routes, customer_routes, sale_routes

# 👇 Create FastAPI app first
app = FastAPI()

# 👇 Define allowed origins
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# 👇 Then apply CORS middleware to the `app`
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Or use ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

# 👇 Include your routers
app.include_router(product_routes.router,
                   prefix="/products", tags=["Products"])
app.include_router(category_routes.router,
                   prefix="/categories", tags=["Categories"])
app.include_router(customer_routes.router,
                   prefix="/customer", tags=["Customers"])
app.include_router(sale_routes.router, prefix="/saleOrder", tags=["SaleOrder"])

app.mount("/static", StaticFiles(directory="static"), name="static")
