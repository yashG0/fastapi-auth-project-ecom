from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware   
from .routers import productRoute
from .routers import authRoute, userRoute
from .db import Base,engine


Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Allow CORS for specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

@app.get("/")
async def getHomePage(req:Request):
    return templates.TemplateResponse(name="home.html" ,context={"request":req})


app.include_router(router=authRoute.authRoutes)
app.include_router(router=userRoute.userRoutes) 
app.include_router(router=productRoute.productRouters)