import random
import secrets
import contextvars

from fastapi import FastAPI
from starlette.responses import RedirectResponse, Response

from .generators import Generator

app = FastAPI()


@app.get("/{rules}")
def get_random(rules: str):
    """Redirect back with a new random seed."""
    seed = secrets.token_urlsafe()
    return RedirectResponse(url=f"/{rules}/{seed}")


@app.get("/{rules}/{seed}")
async def get_seeded(rules: str, seed: str):

    # Choose which generator to use
    generator = Generator.from_rules(rules, seed)
    if not generator:
        return Response(status_code=404)

    # Execute generator and return character data
    return generator.generate()
