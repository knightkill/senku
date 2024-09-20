import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import subprocess
from langchain_core.pydantic_v1 import BaseModel, Field
import os
from datetime import datetime



if __name__ == "__main__":
    app = MermaidApp()
    app.main()
