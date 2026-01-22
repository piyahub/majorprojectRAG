
from fastapi import APIRouter, Depends, BackgroundTasks
from app.core.auth import admin_required
from app.services.mongo_ingest_service import ingest_selected_collections

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/ingest")
def ingest_endpoint(
    background_tasks: BackgroundTasks,
    _: str = Depends(admin_required)
):
    background_tasks.add_task(ingest_selected_collections)
    return {"status": "Ingestion started in background"}

