import sys
from pathlib import Path

# Ensure the project root is on sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import os
from backend.app import create_app
from backend.config import Config

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n=======================================================")
    print(f"  PocketSmart AI 2.0 Server running at http://127.0.0.1:{port}")
    print(f"  Luxury Fintech x AI Assistant Platform")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
