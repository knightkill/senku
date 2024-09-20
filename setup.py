from setuptools import setup, find_packages

setup(
    name='mermaid_diagram_generator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'langchain',
        'langchain-openai',
        'python-dotenv',
        'datasets',
        'huggingface_hub',
    ],
    entry_points={
        'console_scripts': [
            'mermaid_app = src.run_app:run'
        ]
    }
)