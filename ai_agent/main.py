import os
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from ai_agent.indexing.indexer import Indexer
from ai_agent.rag.qa_service import QAService
from ai_agent.ag_ui.router import AgUiRoute, AgUiResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Move to a proper config file
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

    indexer = Indexer()
    app.state.indexer = indexer
    app.state.qa_service = QAService(openrouter_api_key=OPENROUTER_API_KEY, indexer=indexer)
    yield

app = FastAPI(lifespan=lifespan)
router = APIRouter(route_class=AgUiRoute)

class QueryRequest(BaseModel):
    query: str

@app.get("/api/v1/status")
def get_status():
    return {"status": app.state.indexer.get_status()}

@app.post("/api/v1/index")
def start_indexing():
    import threading
    thread = threading.Thread(target=app.state.indexer.run_full_index)
    thread.start()
    return {"message": "Indexing started in the background."}

@router.post("/api/v1/query")
def query(request: QueryRequest):
    task_id = str(uuid.uuid4())
    result = app.state.qa_service.answer_query(request.query)

    events = [
        {"type": "task_start", "task_id": task_id},
        {"type": "result", "task_id": task_id, "result": result['answer']}
    ]

    for match in result['matches']:
        for image_path in match['images']:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            import base64
            events.append({
                "type": "artifact",
                "task_id": task_id,
                "artifact_id": str(uuid.uuid4()),
                "mime_type": "image/png",
                "data": base64.b64encode(image_data).decode('utf-8')
            })

    events.append({"type": "task_end", "task_id": task_id})

    return AgUiResponse(content=events)

app.include_router(router)
