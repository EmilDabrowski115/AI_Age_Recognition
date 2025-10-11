import uvicorn
from backend.app import app
from backend.database.database import initalize_database


if __name__ == "__main__":
    # Initialize DB first
    initalize_database()

    # Then start the server
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
