# Cognify - Development Setup Guide

This guide provides instructions to set up and run the Cognify project locally.

## Prerequisites
- **Git**
- **Python** 3.9+ and Pip
- **Node.js** v18+ and npm
- **ffmpeg**: Required for audio processing.
    - **macOS (via Homebrew):** `brew install ffmpeg`
    - **Windows (via Chocolatey):** `choco install ffmpeg`
    - **Linux (via apt):** `sudo apt update && sudo apt install ffmpeg`

## Installation
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-team/cognify-project.git
    cd cognify-project
    ```
2.  **Set Up Backend Environment:**
    ```bash
    # Navigate to the backend directory
    cd backend

    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `.\venv\Scripts\activate`

    # Install Python dependencies
    pip install -r requirements.txt

    # Download SpaCy model
    python -m spacy download en_core_web_sm
    ```
3.  **Set Up Frontend Environment:**
    ```bash
    # Navigate to the frontend directory from the project root
    cd ../frontend

    # Install Node.js dependencies
    npm install
    ```
4.  **Configure Environment Variables:**
    *In the root directory, copy the example environment file. No keys are needed for V1.0, but this step is important.*
    ```bash
    cp .env.example .env
    ```

## Running the Application
You will need two separate terminal windows to run both the backend and frontend servers simultaneously.

**Terminal 1: Start the Backend**
```bash
# From the project root, navigate to the backend
cd backend

# Activate the virtual environment
source venv/bin/activate

# Run the FastAPI server
uvicorn main:app --reload