from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.main.loaders.loaders import loader

from src.main.routes import machine_routes


def application() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await loader()
        yield
        # end

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(machine_routes.router)

    return app
