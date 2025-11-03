# Backend AI Agent for Q&A over Private Documents

## 1. Project Overview

This project is a backend-only AI agent designed for robust Question & Answering over a private document base. The agent connects to document sources like Google Drive and Microsoft SharePoint, indexes their content into a vector database, and provides synthesized answers to user queries.

The key technical differentiators for this project are:
- **ag-ui Protocol:** All communication with the agent is handled via the standard ag-ui (Agent-User Interaction Protocol), ensuring a standardized and extensible interface.
- **Image Artifact Output:** A critical feature is the dynamic generation of PNG images. The API response includes not only the text answer but also "screenshots" of the original document sections (PDF, DOCX, XLSX, etc.) with the relevant text visually highlighted.

---

## 2. Core Functional Requirements

### 2.1. Document Ingestion and Synchronization

-   **Modular Sources:** The agent ingests documents from a single source at a time (Google Drive or SharePoint), configured via environment variables.
-   **File Format Support:** The agent can parse and index the following file types:
    -   `pdf`
    -   `pptx`
    -   `xlsx`
    -   `docx`
    -   `md`
    -   `.html`
    -   `.txt`
-   **Indexing Process:**
    -   **Initial Indexing:** On startup, the agent performs a full indexing of the configured document repository.
    -   **Status Endpoint:** A status endpoint at `/api/v1/status` provides real-time updates on the indexing process (e.g., "Connecting", "Indexing {X/Y} docs", "Complete").
    -   **Synchronization:** The agent includes a mechanism for daily or webhook-based synchronization to detect and process new, modified, or deleted files.

### 2.2. Q&A Logic (RAG)

The agent employs an advanced Retrieval-Augmented Generation (RAG) pipeline:
1.  It receives queries (prompts) via its `ag-ui` endpoint.
2.  It searches its internal vector database for the most relevant information chunks to answer the query.
3.  It synthesizes a coherent, complete answer based on information from multiple sources, rather than simply returning raw text chunks.

### 2.3. Artifact Generation (Key Requirement)

Along with the synthesized text answer, the API returns a list of "matches," each containing:
-   A link or unique identifier for the source document.
-   An on-the-fly generated PNG image file.

**Image Specifications:**
-   The image is a "screenshot" of the relevant section of the original document.
-   A visual highlight (e.g., a yellow box) is drawn over the exact text used to generate the answer.
-   The image is generated with sufficient resolution to be easily readable.
-   If a single match spans two pages (e.g., in a PDF), a single continuous image is generated.

---

## 3. Technical Architecture & Proposal

### 3.1. Detailed Tech Stack

-   **Language:** Python (3.10+)
-   **Backend Framework:** **FastAPI**. It is a modern, high-performance web framework for building APIs with Python, with excellent support for asynchronous operations and data validation with Pydantic. It can also support Agent-to-Agent (A2A) communication patterns if required in the future.
-   **Vector Database:** **ChromaDB**. It is an open-source embedding database that can be run embedded within the agent, making the application self-contained with no external database dependency. For larger-scale deployments, it can be easily swapped with a more scalable solution like **pgvector** as suggested.
-   **LLM (Language Model):**
    -   **Router:** **OpenRouter** is used as the single router for all LLM calls.
    -   **Testing Model:** The agent is developed and tested with **`mistralai/Mistral-7B-Instruct-v0.2`**, a powerful open-source model available via OpenRouter.
-   **Document Parsing Libraries:**
    -   `PyMuPDF` for PDF processing.
    -   `python-docx` for `.docx` files.
    -   `openpyxl` for `.xlsx` files.
    -   `python-pptx` for `.pptx` files.
    -   `markdown-it-py` for Markdown.
    -   `BeautifulSoup4` for HTML.
-   **Execution:** The agent is packaged to be executable with **`uvx`**, which handles the creation of an ephemeral virtual environment and runs the application.

### 3.2. Image Generation Strategy (Critical)

To handle the diverse set of file formats, we will employ a two-step "normalize-and-render" strategy:

1.  **Conversion to PDF:** Non-visual formats (`.xlsx`, `.docx`, `.md`, etc.) are first converted into a standardized visual format: PDF. This is achieved by programmatically using the **LibreOffice** suite in headless mode. This approach provides a high-fidelity visual representation of the original document, including formatting, tables, and layout.
2.  **Highlighting and Rendering:** Once the document is in PDF format (either originally or after conversion), we use the **`PyMuPDF`** library.
    -   It searches for the precise location of the text to be highlighted on the PDF page.
    -   It draws a highlight annotation (a yellow rectangle) over the text's coordinates.
    -   It renders the specified page (or pages) into a high-resolution PNG image.

This strategy ensures that the generated image is a true "screenshot" of the document's appearance and that the highlighting is accurate.

### 3.3. Ingestion Approach (MCPs)

As suggested, we will utilize **Model Context Protocol (MCP) servers** to handle the integration with Google Drive and SharePoint. Based on an analysis of existing open-source MCPs, we have determined that building a **custom MCP** for each service is the most effective approach. This allows us to:
-   Tailor the implementation to our specific needs, including webhook-based synchronization.
-   Ensure the long-term maintainability and quality of the integration.
-   Provide a reusable component for future projects.

---

## 4. Installation & Setup

### 4.1. System Dependencies
This project requires **LibreOffice** to be installed on the system for document conversion.

-   **Ubuntu/Debian:**
    ```bash
    sudo apt-get update && sudo apt-get install -y libreoffice
    ```
-   **macOS (using Homebrew):**
    ```bash
    brew install --cask libreoffice
    ```

### 4.2. Application Dependencies
This project uses **Poetry** for dependency management.

1.  **Install Poetry:**
    ```bash
    pip install poetry
    ```
2.  **Install Project Dependencies:**
    ```bash
    poetry install
    ```

## 5. Configuration

Create a `.env` file in the project root and set the following environment variables:

```
# The data source to use ('gdrive' or 'sharepoint')
DATA_SOURCE=gdrive

# OpenRouter API Key
OPENROUTER_API_KEY="your-openrouter-api-key"

# --- Google Drive Configuration ---
# Path to the Google Cloud credentials JSON file
GDRIVE_CREDENTIALS_PATH="/path/to/your/credentials.json"

# --- SharePoint Configuration ---
# SharePoint site URL, client ID, and client secret
SHAREPOINT_URL="https://your-tenant.sharepoint.com/sites/YourSite"
SHAREPOINT_CLIENT_ID="your-sharepoint-client-id"
SHAREPOINT_CLIENT_SECRET="your-sharepoint-client-secret"
```

## 6. Execution

To run the agent server, use the following `uvx` command:

```bash
uvx uvicorn ai_agent.main:app --host 0.0.0.0 --port 8000
```

The agent will now be running and accessible at `http://localhost:8000`.
