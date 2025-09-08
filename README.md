# Diary Bot RAG Assistant

This application creates a Retrieval-Augmented Generation (RAG) system that allows users to ask questions about their custom-made diary. For demonstration, the system uses an arbitrarily created diary, with AI generated entries stored in a .csv file. The script for injecting this data appropriately into a PostgreSQL database with vector embeddings is provided, it enables context-aware responses to user queries.

<div align="center">
  <h3>🖥️ Gradio Web Interface</h3>
  <img src="https://raw.githubusercontent.com/JoeCardoso13/JoeCardoso13/main/assets/Diary_Bot_Gradio_UI4_1.gif" alt="Gradio UI Demonstration" width="100%" style="max-width: 800px; border-radius: 10px; border: 2px solid #e1e4e8; box-shadow: 0 6px 12px rgba(0,0,0,0.1);">
  <img src="https://raw.githubusercontent.com/JoeCardoso13/JoeCardoso13/main/assets/Diary_Bot_Gradio_UI4_2.gif" alt="Gradio UI Demonstration" width="100%" style="max-width: 800px; border-radius: 10px; border: 2px solid #e1e4e8; box-shadow: 0 6px 12px rgba(0,0,0,0.1);">
</div>

<br><br>

<div align="center">
  <h3>⌨️ Command Line Interface</h3>
  <img src="https://raw.githubusercontent.com/JoeCardoso13/JoeCardoso13/main/assets/Diary_Bot_CLI3.gif" alt="CLI Demonstration" width="100%" style="max-width: 800px; border-radius: 10px; border: 2px solid #e1e4e8; box-shadow: 0 6px 12px rgba(0,0,0,0.1);">
</div>

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ with pgvector extension
- OpenAI API key

## Installation

1. Clone this repository and change directory to its root folder:
```bash
git clone https://github.com/JoeCardoso13/diary_bot.git && cd diary_bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
   - Install PostgreSQL if you haven't already
   - Install the pgvector extension:
     ```sql
     CREATE EXTENSION vector;
     ```
   - Create a database named `diary_bot`

5. Add your OpenAI API key into your environment, e.g. an `.env` file with the following:
```
OPENAI_API_KEY=your_api_key_here
DB_NAME=diary_bot
DB_USER=your_psql_user_name
DB_HOST=/var/run/postgresql_or_localhost
DB_PORT=5432
```

## Data Processing

Before using the system, you need to process the diary entries by running the `pre_processing.py` script:

```bash
python src/pre_processing.py
```

This will:
- Read the CSV file
- Generate embeddings for each entry
- Store the data in the PostgreSQL database

## Running the Application

### Option 1: Web Interface

Run the Gradio interface for a user-friendly web experience:
```bash
python src/main_gradio_interface.py
```

This will:
- Start a local web server
- Open the interface in your default browser
- Allow you to:
  - Ask questions about my hike
  - Get random question suggestions
  - See responses with source attribution

### Option 2: Command Line Interface

Run the CLI version for a simpler interface:
```bash
python src/main_command_line.py
```

This provides:
- A text-based interface
- Same functionality as the web version
- Responses in the terminal

## Project Structure

```
diary_bot/
├── data/
│   └── diary.csv    # Blog entries data
├── src/
│   ├── pre_processing.py    # Data processing and embedding generation
│   ├── rag_tools.py        # Shared RAG functionality
│   ├── main_command_line.py # CLI interface
│   └── main_gradio_interface.py # Web interface
├── requirements.txt        # Python dependencies
└── README.md
```

## Database Schema

The `diary` table contains:
- `id`: Unique identifier
- `date`: Date of diary entry
- `entry`: Content of diary entry
- `embedding`: Vector embedding of the entry text

