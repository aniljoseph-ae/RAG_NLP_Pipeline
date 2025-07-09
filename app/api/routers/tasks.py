from fastapi import APIRouter, HTTPException
from app.database import vector_db
import logging

router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)

@router.get("/vector/snapshots")
def list_snapshots():
    try:
        
        return {
            "snapshots": [
                {"id": "snap-001", "name": "initial-snapshot", "created_at": "2024-01-01"},
                {"id": "snap-002", "name": "pre-update-snapshot", "created_at": "2024-02-01"}
            ]
        }
    except Exception as e:
        logger.error(f"Snapshot listing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/vector/snapshots", status_code=201)
def create_snapshot():
    versioning = vector_db.VectorVersioning()
    return versioning.create_snapshot("nlp_documents")

@router.post("/vector/snapshots/{snapshot_id}/restore")
def restore_snapshot(snapshot_id: str):
    versioning = vector_db.VectorVersioning()
    return versioning.restore_snapshot(snapshot_id)