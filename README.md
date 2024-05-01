# TAKE-HOME

Create APIs to store path and folder of all uploaded files


## Installation

1. Clone the repository:

    ```bash
    https://github.com/neerajshukla165/take-home-demo.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Access the API documentation:

    Open your web browser and go to [http://localhost:8000/docs](http://localhost:8000/docs).

## Project Structure

- `main.py`: Entry point of the FastAPI application.
- `db/`: Directory containing database-related files.
  - `__init__.py`: Package initialization file.
  - `connection.py`: Database connection functions.
  - `models.py`: Pydantic models for database tables.
- `routers/`: Directory containing router modules for API endpoints.
  - `__init__.py`: Package initialization file.
  - `take_home_file.py`: Router for file-related endpoints.
  - `take_home_folder.py`: Router for folder-related endpoints.
- `README.md`: This file

