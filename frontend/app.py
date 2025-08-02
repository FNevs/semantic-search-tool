import streamlit as st
import requests
import json
import os

# Set the backend URL
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Lattes XML Processor", layout="wide")

st.title("Lattes XML Processor")

st.markdown("""
### Upload Lattes XML files and search for publications

This application allows you to:
1. Upload multiple Lattes curriculum XML files
2. Process them to extract researcher information and publications
3. Search for publications by keywords
""")

# Create tabs for upload and search
tab1, tab2 = st.tabs(["Upload XML Files", "Search Publications"])

with tab1:
    st.header("Upload Lattes XML Files")
    
    # File uploader for multiple XML files
    uploaded_files = st.file_uploader("Choose Lattes XML files", accept_multiple_files=True, type=['xml'])
    
    if st.button("Process Files") and uploaded_files:
        with st.spinner("Processing XML files..."):
            # Prepare files for upload
            files = []
            for uploaded_file in uploaded_files:
                files.append(("files", (uploaded_file.name, uploaded_file.getvalue(), "text/xml")))
            
            try:
                # Send files to backend
                response = requests.post(f"{BACKEND_URL}/process-xmls", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Successfully processed {result['message']}")
                    st.json(result)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Make sure it's running at " + BACKEND_URL)
    
    if not uploaded_files:
        st.info("Please upload one or more Lattes XML files to process.")

with tab2:
    st.header("Search Publications")
    
    # Add search mode selection
    search_mode = st.radio(
        "Search by:",
        ["Search by Publication Title", "Search by Author Name"]
    )
    
    # Search input
    search_query = st.text_input("Enter search term")
    
    if st.button("Search") and search_query:
        with st.spinner("Searching..."):
            try:
                # Determine which endpoint to use based on search mode
                if search_mode == "Search by Publication Title":
                    endpoint = "/search"
                    params = {"query": search_query}
                else:  # Search by Author Name
                    endpoint = "/search-by-author"
                    params = {"name": search_query}
                
                # Send search query to backend
                response = requests.get(f"{BACKEND_URL}{endpoint}", params=params)
                
                if response.status_code == 200:
                    results = response.json()
                    
                    if results:
                        search_type = "publication title" if search_mode == "Search by Publication Title" else "author name"
                        st.subheader(f"Found {len(results)} results for {search_type} '{search_query}'")
                        
                        # Display results in a nice format
                        for i, result in enumerate(results, 1):
                            with st.expander(f"{i}. {result['title']}"):
                                st.markdown(f"**Researcher:** {result['researcher']}")
                                st.markdown(f"**Title:** {result['title']}")
                    else:
                        search_type = "publication titles" if search_mode == "Search by Publication Title" else "author names"
                        st.info(f"No {search_type} found matching '{search_query}'")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Make sure it's running at " + BACKEND_URL)
    
    if not search_query:
        st.info("Enter a search term to find publications.")

# Footer
st.markdown("---")
st.markdown("""
### How to use this application

1. **Upload Tab**: Upload one or more Lattes XML files and click "Process Files" to extract and store the data.
2. **Search Tab**: Enter keywords to search for publications in the processed data.

**Note**: Make sure the backend server is running at {}.
""".format(BACKEND_URL))