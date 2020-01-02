import random
import secrets
import contextvars

from fastapi import FastAPI
from starlette.responses import RedirectResponse, Response

import chargen

app = FastAPI()


@app.get("/{api}")
def get_random(api: str):
    """Redirect back with a new random seed."""
    seed = secrets.token_urlsafe()
    return RedirectResponse(url=f"/{api}/{seed}")


@app.get("/{api}/{seed}")
async def get_seeded(api: str, seed: str):

    # Choose which generator to use
    if api == "cod":
        gen = chargen.CoDGen
    elif api == "mtaw2":
        gen = chargen.Mage2eGen
    else:
        return Response(status_code=404)

    # Execute generator and return character data
    return gen(seed).generate()
