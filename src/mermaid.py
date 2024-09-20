import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import subprocess
from langchain_core.pydantic_v1 import BaseModel, Field
import os
from datetime import datetime


class ProcessPrompt(BaseModel):
    instruction = """
    Prompt to generate Mermaid code for a following process or task:
    Task: {task}
    """
    prompt: str = Field(description="")


class LLMHandler:
    def __init__(self):
        self.llm = ChatOpenAI(model="ft:gpt-4o-mini-2024-07-18:anormaly-labs::9zdIrrcb")
        self.mini_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.mini_llm.with_structured_output(ProcessPrompt, method="json_mode")

    def generate_mermaid_code(self, text_section):
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

        chain = prompt | self.llm | StrOutputParser()
        mermaid_code = chain.invoke({"text_section": text_section})
        return mermaid_code.strip()

    def generate_mermaid_prompt(self, task):
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

        mermaid_code = self.mini_llm.invoke(prompt_template.format(task=task))
        print(mermaid_code)
        return mermaid_code.content


class MermaidHandler:
    @staticmethod
    def convert_mermaid_to_image(mermaid_code):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"./output/{timestamp}"
        os.makedirs(output_dir, exist_ok=True)

        mermaid_file = f"{output_dir}/diagram.mmd"
        output_file = f"{output_dir}/diagram.png"

        with open(mermaid_file, "w") as f:
            f.write(mermaid_code)

        try:
            subprocess.run(
                ["mmdc", "-i", mermaid_file, "-o", output_file, "--theme", "dark", "--width", "1920"],
                check=True,
            )
            return output_file
        except subprocess.CalledProcessError as e:
            st.error("Failed to generate the diagram image.")
            st.error(str(e))
            return None


class MermaidApp:
    def __init__(self):
        self.llm_handler = LLMHandler()
        self.mermaid_handler = MermaidHandler()

    def main(self):
        st.title("Mermaid Diagram Generator")

        if 'task' not in st.session_state:
            st.session_state.task = "Coffee Brewing System"

        task_section = st.text_area("Task/Process Name", value=st.session_state.task, key="task")

        if 'prompt' not in st.session_state:
            st.session_state.prompt = """
            I am a coffee brewing system that operates in a few distinct steps. First, 
            I start by gathering all the necessary ingredients: fresh coffee beans, water, and a coffee filter. Once I 
            have everything ready, I begin with the grinding process, where I grind the coffee beans to a medium 
            consistency. After the beans are ground, I move on to the brewing stage. I measure the correct amount of 
            water and heat it to the optimal temperature of about 200°F (93°C). Once the water is ready, I pour it over 
            the ground coffee in the filter, allowing the water to extract the flavors as it drips into the carafe below. 
            Finally, after brewing for about four to five minutes, I have a fresh pot of coffee ready to serve. I can 
            then pour the coffee into a cup and add milk or sugar according to preference.
            """

        if st.button("Improve Prompt"):
            st.session_state.prompt = self.llm_handler.generate_mermaid_prompt(st.session_state.task)

        text_section = st.text_area("Text Section to Describe", value=st.session_state.prompt, key="prompt")

        if st.button("Generate Mermaid Diagram"):
            with st.spinner("Generating Mermaid code..."):
                mermaid_code = self.llm_handler.generate_mermaid_code(st.session_state.prompt)
                st.code(mermaid_code, language="mermaid")

                st.write("Converting Mermaid code to image using Mermaid CLI...")
                image_path = self.mermaid_handler.convert_mermaid_to_image(mermaid_code)

                if image_path:
                    st.image(image_path, caption="Generated Mermaid Diagram")


if __name__ == "__main__":
    app = MermaidApp()
    app.main()
