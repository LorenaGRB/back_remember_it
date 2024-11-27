from fastapi import FastAPI
from app.routes import sentence_route, user_route, word_route
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(word_route.router, prefix="/words", tags=["Words"])
app.include_router(sentence_route.router, prefix="/sentences", tags=["Sentences"])