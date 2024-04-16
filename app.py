import streamlit as st
import openai

# Set up OpenAI API key
file = open('key.txt')
key = file.read().strip()  # Strip whitespace and newlines
openai.api_key = key
file.close()

# Define custom CSS
custom_css = """
<style>
body {
    background-color: #f0f2f6;
    color: #333;
    font-family: Arial, sans-serif;
}
.stButton button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    border-radius: 5px;
    border: none;
}
.stButton button:hover {
    background-color: #45a049;
}
</style>
"""

# Streamlit UI
def main():
    # Add custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    st.title("Python Code Reviewer")
    st.write("Welcome to the Python Code Reviewer app! Enter your Python code below and click 'Submit' to get suggestions for improvement.")

    # Input box for user to submit Python code
    code = st.text_area("Enter your Python code here:", height=200)

    if st.button("Submit"):
        # Call function to analyze code
        analyze_code(code)

# Function to analyze code using OpenAI API
def analyze_code(code):
    try:
        # Call OpenAI API to analyze code
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "Scan the Python code and identify any mistakes or areas for improvement:"},
                {"role": "user", "content": code}
            ]
        )

        # Get the fixed code snippet from the API response
        fixed_code = response.choices[0].message['content'].strip()

        # Check if the corrected code separator exists
        if "The corrected code should be:\n" in fixed_code:
            description, corrected_code = fixed_code.split("The corrected code should be:\n", 1)

            st.subheader("Description of Mistake:")
            st.write(description.strip())
            
            st.subheader("Corrected Code:")
            st.code(corrected_code.strip(), language="python")
            
        else:
            st.subheader("Description:")
            st.write(fixed_code.strip())

    except Exception as e:
        st.error("Error analyzing code: {}".format(e))

if __name__ == "__main__":
    main()
