from langchain_core.pydantic_v1 import BaseModel, Field


class ProcessPrompt(BaseModel):
    """
    Represents a prompt for generating Mermaid code for a given process or task.
    """
    prompt: str = Field(description="The actual prompt to generate Mermaid code.")
