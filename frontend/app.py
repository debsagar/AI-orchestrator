import streamlit as st
import requests
from requests.exceptions import RequestException
import pandas as pd

API_URL = "http://localhost:8000"

st.title("AI Orchestrator UI")

# File upload section
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Read and show sample of uploaded file
    df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded file:")
    st.write(df.head())
    
    if st.button("Clean Dataset"):
        try:
            # Convert DataFrame to CSV string
            csv_string = df.to_csv(index=False)
            
            # Send request with CSV data
            response = requests.post(
                f"{API_URL}/process_request",
                json={
                    "request": "Clean this dataset",
                    "data": csv_string
                }
            )
            response.raise_for_status()
            st.write("Response:", response.json())
        except RequestException as e:
            st.error(f"Error communicating with API: {str(e)}")
        except ValueError as e:
            st.error(f"Error parsing response: {str(e)}")

# Regular text input for other tasks
user_input = st.text_area("Or enter a text request:")
if st.button("Submit Request"):
    try:
        response = requests.post(
            f"{API_URL}/process_request", 
            json={"request": user_input}
        )
        response.raise_for_status()
        st.write("Response:", response.json())
    except RequestException as e:
        st.error(f"Error communicating with API: {str(e)}")
    except ValueError as e:
        st.error(f"Error parsing response: {str(e)}")

task_id = st.text_input("Enter Task ID to check status:")

if st.button("Check Status"):
    try:
        response = requests.get(f"{API_URL}/status/{task_id}")
        response.raise_for_status()
        st.write("Task Status:", response.json())
    except RequestException as e:
        st.error(f"Error checking status: {str(e)}")

if st.button("Get Results"):
    try:
        response = requests.get(f"{API_URL}/results/{task_id}")
        response.raise_for_status()
        st.write("Task Results:", response.json())
    except RequestException as e:
        st.error(f"Error getting results: {str(e)}")
