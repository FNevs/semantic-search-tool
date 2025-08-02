# Lattes XML Processor

This is a full-stack Python application that processes Lattes curriculum XML files. It extracts researcher information and their publications, stores them in a SQLite database, and provides a search interface.

## Project Structure

```
/TEES
  /backend           # FastAPI backend application
    main.py          # Main backend code
    requirements.txt # Backend dependencies
  /frontend          # Streamlit frontend application
    app.py           # Main frontend code
    requirements.txt # Frontend dependencies
  README.md          # This file
```

## Features

- Upload and process multiple Lattes XML files
- Extract researcher names and publication titles
- Store data in a SQLite database
- Search for publications by keywords or author names
- Display search results with researcher information

## Requirements

- Python 3.8 or higher
- FastAPI (backend)
- Streamlit (frontend)
- Other dependencies listed in the requirements.txt files

## Setup and Installation

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

   The backend server will start at http://localhost:8000

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

   The frontend application will open in your default web browser at http://localhost:8501

## How to Use

1. Start both the backend and frontend servers as described above.

2. In your web browser, go to http://localhost:8501 to access the Streamlit interface.

3. In the "Upload XML Files" tab:
   - Upload one or more Lattes XML files using the file uploader.
   - Click the "Process Files" button to send the files to the backend for processing.
   - The backend will extract researcher names and publication titles and store them in the database.

4. In the "Search Publications" tab:
   - Select the search mode: "Search by Publication Title" or "Search by Author Name".
   - Enter a search term in the text input field.
   - Click the "Search" button to search for publications based on the selected mode.
   - The results will display the matching publication titles and the names of the researchers.

## API Endpoints

- `POST /process-xmls`: Accepts multiple XML files, extracts data, and stores it in the database.
- `GET /search?query=<search_term>`: Searches for publications containing the specified term.
- `GET /search-by-author?name=<author_name>`: Searches for all publications by authors whose names contain the specified term.

## Notes

- The backend uses a SQLite database file named `lattes.db` which is created automatically in the backend directory.
- The frontend is configured to connect to the backend at http://localhost:8000. If you change the backend address or port, update the `BACKEND_URL` variable in the frontend's `app.py` file.

## Troubleshooting

- If you encounter connection errors in the frontend, make sure the backend server is running.
- If the backend fails to process XML files, check that they are valid Lattes curriculum XML files with the expected structure.