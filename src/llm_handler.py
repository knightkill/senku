from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.models import ProcessPrompt

class LLMHandler:
    """
    Handles interactions with the language model to generate Mermaid code and prompts.
    """
    def __init__(self):
        self.finetuned_model = ChatOpenAI(model="ft:gpt-4o-mini-2024-07-18:anormaly-labs::9zdIrrcb")
        self.base_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.base_model.with_structured_output(ProcessPrompt, method="json_mode")

    def generate_mermaid_code(self, text_section):
        """
        Generates Mermaid code from a given text section using the language model.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Convert the following instruction into a very detailed Mermaid diagram in Markdown format. "
                       "The diagram type (flowchart, sequence, class, etc.) should be determined contextually "
                       "based on the instruction content. Ensure that all relevant details, relationships, "
                       "decision points, and interactions are represented clearly and accurately. The output "
                       "should be solely the Mermaid diagram code, without any extra information, explanations, "
                       "or formatting beyond what is required for the diagram itself. Please give detailed diagrams "
                       "or I will fire you."),
            ("human", "{text_section}"),
        ])

        chain = prompt | self.finetuned_model | StrOutputParser()
        mermaid_code = chain.invoke({"text_section": text_section})
        return mermaid_code.strip()

    def generate_mermaid_prompt(self, task):
        """
        Generates a detailed description of a process or system for a given task using the language model.
        """
        prompt_template = """
        Generate a detailed description of a process or system of a given task in a first-person perspective. 
        The task should involve multiple steps, decisions, and interactions between components. 
        It should cover the flow of actions, possible conditions, and outcomes, and should be structured 
        in a way that can be represented using sub-diagrams or sub-graphs with or without interconnections. 
        The description should be detailed enough to allow the creation of a complex flowchart or diagram 
        using these sub-sections. Ensure that only the task description is provided, without any additional information. 
        Use the task below:

        Task: {task}
        """

        mermaid_code = self.base_model.invoke(prompt_template.format(task=task))
        print(mermaid_code)
        return mermaid_code.content