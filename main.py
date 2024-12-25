from fastapi import FastAPI
from application import api_router
from uvicorn import Config, Server

app = FastAPI()
app.include_router(api_router)
config = Config(
    app=app,
    host="localhost",
    port=8081
)

server = Server(config)
server.run()