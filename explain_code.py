import streamlit as st
import openai
import os  
#do this to load the env variables
from dotenv import load_dotenv
load_dotenv()
# Set up OpenAI API credentials
# Set up OpenAI API credentials
openai.api_type = "azure"

openai.api_base = 'https://xxxxxxx.openai.azure.com/'
openai.api_version = "2023-03-15-preview"

#option1 create a stremline secretes 

#option1 create a stremline secretes 
#Option # 1 - Using Streamlit secrets
#This is the easiest way using Streamlit secrets : 
#1.Create a folder within your director where you have the code name as “.streamlit “
#2.Create a file name as “ secrets.toml” under the folder “.streamlit “
#3. Assign the key in the “ secrets.toml”
#Path = '363e5eaaaaaabbbbbccccc'
#Flow will look like this : projectfolder\streamlit\.streamlit
#When you call the key within your code use this :  openai.api_key = st.secrets['path']

openai.api_key = st.secrets['path']

#using option#2 env variable 
#openai.api_key = os.getenv("OPENAI_API_KEY")

#openai.api_key_path = 'key.env'


# option#3 hard code the key 
#openai.api_key = 'xxxxxxxxxxxxxxxxxxxxxx<your key>'

# Define Streamlit app layout
st.title("Code Explainer")
language = st.selectbox("Select Language", ["Python", "JavaScript"])
code_input = st.text_area("Enter code to explain")



# Define function to explain code using OpenAI Codex
def explain_code(input_code, language):
    model_engine = "text-davinci-002" # Change to the desired OpenAI model
    prompt = f"Explain the following {language} code: \n\n{input_code}"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text

# Temperature and token slider
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.1
)
tokens = st.sidebar.slider(
    "Tokens",
    min_value=64,
    max_value=2048,
    value=256,
    step=64
)
# Define Streamlit app behavior
if st.button("Explain"):
    output_text = explain_code(code_input, language)
    st.text_area("Code Explanation", output_text)
