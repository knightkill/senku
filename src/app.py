import streamlit as st
from src.llm_handler import LLMHandler
from src.mermaid_handler import MermaidHandler


# Rest of your app.py code

class MermaidApp:
    """
    Represents the main application for generating Mermaid diagrams from text descriptions.
    """

    def __init__(self):
        self.llm_handler = LLMHandler()
        self.mermaid_handler = MermaidHandler()

    def main(self):
        """
        Runs the main application logic.
        """
        st.title("Senku - The Diagram Generator")
        st.markdown('<style>h1 {color: red;}</style>', unsafe_allow_html=True)

        if 'task' not in st.session_state:
            st.session_state.task = "Coffee Brewing System"

        task_section = st.text_input("Task/Process Name", key="task")

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

        text_section = st.text_area("Text Section to Describe", key="prompt")

        if st.button("Generate Mermaid Diagram"):
            with st.spinner("Generating Mermaid code..."):
                mermaid_code = self.llm_handler.generate_mermaid_code(st.session_state.prompt)
                st.code(mermaid_code, language="mermaid")

                st.write("Converting Mermaid code to image using Mermaid CLI...")
                image_path = self.mermaid_handler.convert_mermaid_to_image(mermaid_code)

                if image_path:
                    st.image(image_path, caption="Generated Mermaid Diagram")


def main():
    app = MermaidApp()
    app.main()


if __name__ == "__main__":
    main()
