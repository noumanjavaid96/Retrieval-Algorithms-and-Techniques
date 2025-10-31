# AI Agent for Q&A over Private Documents

This is a backend-only AI agent designed for Q&A over a private document base. The agent connects to document sources (initially SharePoint or Google Drive), indexes their content, and answers user queries.

## Features

- **Document Ingestion:** Ingests documents from Google Drive.
- **File Format Support:** Supports pdf, pptx, xlsx, docx, md, html, and txt.
- **Q&A Logic (RAG):** Uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions.
- **Image Artifact Output:** Generates PNG "screenshots" of the original document sections with the relevant text highlighted.
- **ag-ui Protocol:** All communication with the agent is handled via the standard ag-ui (Agent-User Interaction Protocol).
- **OpenRouter Integration:** Uses OpenRouter for all LLM calls.

## Installation

1.  **Install LibreOffice:**
    This project requires LibreOffice to be installed on the system to convert office documents to PDF.
    -   **Ubuntu/Debian:**
        ```bash
        sudo apt-get install libreoffice
        ```
    -   **macOS (using Homebrew):**
        ```bash
        brew install --cask libreoffice
        ```
    -   **Windows (using Chocolatey):**
        ```bash
        choco install libreoffice
        ```

2.  **Install poetry:**
    ```bash
    pip install poetry
    ```
3.  **Install dependencies:**
    ```bash
    poetry install
    ```

## Configuration

1.  **Google Drive API Credentials:**
    *   Follow the steps [here](https://developers.google.com/drive/api/v3/quickstart/python) to enable the Google Drive API and download your `credentials.json` file.
    *   Place the `credentials.json` file in the root of the project.
    *   The first time you run the agent, you will be prompted to authenticate with your Google account. A `token.pickle` file will be created to store your credentials for future use.
2.  **OpenRouter API Key:**
    *   Sign up for an account at [OpenRouter](https://openrouter.ai/).
    *   Create an API key.
    *   Set the `OPENROUTER_API_KEY` environment variable:
        ```bash
        export OPENROUTER_API_KEY="your-api-key"
        ```

## Execution

To run the agent, use `uvx`:

```bash
uvx uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

-   **`POST /api/v1/index`**: Starts the document indexing process.
-   **`GET /api/v1/status`**: Returns the current status of the indexing process.
-   **`POST /api/v1/query`**: Receives a query and returns an `ag-ui` event stream with the answer and image artifacts.

### Query Request Body

```json
{
    "query": "Your question here"
}
```
