import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "0") == "1"
    uvicorn.run(
        "src.interface_adapter.presenters.webhook_api:app",
        host="127.0.0.1",
        port=port,
        reload=reload,
    )
