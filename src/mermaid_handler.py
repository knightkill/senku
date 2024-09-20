import os
import subprocess
import streamlit as st
from datetime import datetime

class MermaidHandler:
    """
    Handles the conversion of Mermaid code to an image using the Mermaid CLI.
    """
    @staticmethod
    def convert_mermaid_to_image(mermaid_code):
        """
        Converts Mermaid code to an image using the Mermaid CLI.
        """
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