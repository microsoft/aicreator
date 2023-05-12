import os
import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Code Converter", page_icon=":computer:")

# Authenticate with OpenAI API
openai.api_type = "azure"
openai.api_base = 'https://xxxxxxxx.openai.azure.com/'
openai.api_version = "2023-03-15-preview"
#openai.api_key = 'xxxxxxxxxxxxxxxxxxxxx'
openai.api_key = st.secrets['path']
model_engine = "text-davinci-002"

# Language selection
source_languages = {
    "Spark 2.0" :  "Spark 2.0", 
    "Python": "Python",
    "JavaScript": "javascript",
    "Java": "java",
    "SQL": "SQL",
    "TSQL": "TSQL",
    "MYSQL":"MY SQL",
    "Oracle":"Oracle" ,
    "PHP" :"PHP",
    "GO": "GO"
}
target_languages = {
    "Spark 3.0" :  "Spark 3.0", 
    "Python": "Python",
    "JavaScript": "javascript",
    "Java": "java",
    "SQL": "SQL",
    "TSQL": "TSQL",
    "MYSQL":"MYSQL",
    "Oracle":"Oracle" ,
     "GO": "GO"
}

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

# User inputs
source_language = st.sidebar.selectbox("Select source language", list(source_languages.keys()))
target_language = st.sidebar.selectbox("Select target language", list(target_languages.keys()))
source_folder = st.sidebar.text_input("Enter source folder location")
target_folder = st.sidebar.text_input("Enter target folder location")

# Conversion function
def convert_file(source_code, source_language, target_language):
    response = openai.Completion.create(
        #engine="text-davinci-002",
        engine="code-davinci-002",
        prompt=f"Convert {source_language} code to {target_language}:\n\n```{source_language}\n{source_code}\n```",
        temperature=temperature,
        max_tokens=tokens,
        n=1,
        stop=None,
        timeout=20,
    )

    return response.choices[0].text.strip()

# Convert files
if st.sidebar.button("Convert"):
    for filename in os.listdir(source_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(source_folder, filename), "r") as f:
                source_code = f.read()
            target_code = convert_file(source_code, source_languages[source_language], target_languages[target_language])
            with open(os.path.join(target_folder, f"{filename.split('.')[0]}_{source_language}_to_{target_language}.txt"), "w") as f:
                f.write(target_code)
            st.success(f"File {filename} converted successfully and saved as {filename.split('.')[0]}_{source_language}_to_{target_language}.txt in {target_folder}")

# Streamlit interface
st.title("Code Converter")

st.sidebar.markdown("### Options")

st.sidebar.markdown("#### Language selection")
st.sidebar.write("Source language:", source_language)
st.sidebar.write("Target language:", target_language)

st.sidebar.markdown("#### File selection")
st.sidebar.write("Source folder location:", source_folder)
st.sidebar.write("Target folder location:", target_folder)

st.sidebar.markdown("### Conversion options")

st.sidebar.markdown("#### Model settings")
st.sidebar.write("Temperature:", temperature)
st.sidebar.write("Tokens:", tokens)

st.markdown("---")

st.write("### Instructions")

st.write("1. Select the source language and target language from the dropdown lists in the sidebar.")
st.write("2. Enter the location of the source folder containing the files you want to convert.")
st.write("3. Enter the location of the target folder to save the converted files.")
st.write("4. Adjust the temperature and tokens sliders to fine-tune the conversion.")
st.write("5. Click the 'Convert' button to begin the conversion process.")
st.write("6. The converted files.")