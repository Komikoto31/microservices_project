from fastapi import FastAPI
from app.endpoints import user_router

app = FastAPI(title='User Service', description='Service for user management and authentication')

app.include_router(user_router, prefix='/api')"# Test comment for CI/CD" 
" " 
