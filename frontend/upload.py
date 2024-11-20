import streamlit as st
import time
import os

def checkFiles():
    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")
        
        file_details = []
        # Display details of uploaded files
        for file in uploaded_files:
        
            file_details.append(
            {"Filename": file.name, "File Size (KB)": round(file.size / 1024, 2)})
            
    
        st.write("Uploaded Files Details:", file_details)

        # Process each file
        for idx, uploaded_file in enumerate(uploaded_files):
            # st.write(f"Processing file {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}")
            st.write(f"Processing file {uploaded_file.name}")

            # Estimate upload time based on `NYn file size
            file_size = uploaded_file.size
            estimated_time = file_size / UPLOAD_SPEED
            st.write(f"Estimated upload time for {uploaded_file.name}: {estimated_time:.2f} seconds")

            # Create a progress bar for each file
            progress_bar = st.progress(0)
            progress_text = st.empty()

            # Simulate upload process for each file
            with st.spinner(f"Uploading {uploaded_file.name}..."):
                for i in range(101):
                    time.sleep(estimated_time / 100)  # Simulate time delay
                    progress_bar.progress(i)
                    progress_text.text(f"{uploaded_file.name}: {i}% completed")

            st.success(f"{uploaded_file.name} uploaded successfully!")
    

# Title of the app
st.title("Code File Upload with Estimated Time")

# # Define upload speed in bytes per second (e.g., 1 MB/s)
UPLOAD_SPEED = 1 * 1024 * 1024  # 1 MB/s

# File uploader widget
uploaded_files = st.file_uploader("Upload your code file", type=["pks", "pkb", "py", "txt"], accept_multiple_files=True)

checkFiles()