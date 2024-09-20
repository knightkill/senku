import streamlit.web.cli as stcli
import sys
from src.app import main

def run():
    sys.argv = ["streamlit", "run", "src/app.py", "--global.developmentMode=false"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    run()