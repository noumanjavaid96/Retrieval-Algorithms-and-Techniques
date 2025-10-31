from unittest.mock import MagicMock
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient
from ai_agent.main import app

def test_status_endpoint():
    # Create a mock indexer
    mock_indexer = MagicMock()
    mock_indexer.get_status.return_value = "Mocked status"

    # Create a mock qa_service
    mock_qa_service = MagicMock()

    @asynccontextmanager
    async def mock_lifespan(app):
        yield

    app.router.lifespan_context = mock_lifespan
    app.state.indexer = mock_indexer
    app.state.qa_service = mock_qa_service

    with TestClient(app) as client:
        response = client.get("/api/v1/status")
        assert response.status_code == 200
        assert response.json() == {"status": "Mocked status"}
