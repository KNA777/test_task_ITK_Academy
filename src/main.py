import sys

import uvicorn
from pathlib import Path

from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api import main_router


app = FastAPI()

app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
