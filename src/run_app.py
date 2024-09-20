import streamlit.web.cli as stcli
import sys
import uvicorn
from src.app import main as streamlit_main
from src.api import app as fastapi_app


def run_streamlit():
    sys.argv = ["streamlit", "run", "src/app.py", "--global.developmentMode=false"]
    sys.exit(stcli.main())


def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8123)


def run():
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_fastapi()
    else:
        run_streamlit()


if __name__ == "__main__":
    run()
