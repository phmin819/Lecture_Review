from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, lectures, reviews, users

app = FastAPI(title="명지전문대 강의 후기 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(lectures.router)
app.include_router(reviews.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Lecture Review API is running"}
