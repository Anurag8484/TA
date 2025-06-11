# run.py

from dotenv import load_dotenv
from app.api.app import app

if __name__ == "__main__":
    load_dotenv()
    app.run(host="0.0.0.0", port=8000, debug=True)
