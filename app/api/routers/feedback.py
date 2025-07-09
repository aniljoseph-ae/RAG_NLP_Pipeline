from fastapi import APIRouter
from app.api.schemas import FeedbackRequest
from app.monitoring.drift_detector import check_feedback_for_drift
import logging

router = APIRouter(tags=["Feedback"])
logger = logging.getLogger(__name__)

@router.post("/feedback", summary="Submit feedback on task results")
def submit_feedback(feedback: FeedbackRequest):
    try:
        # In a real system, store feedback in a database
        logger.info(f"Feedback received for task {feedback.task_id}: Rating {feedback.rating}")
        
        # Check for significant drift
        if feedback.rating < 3:
            check_feedback_for_drift(
                feedback.task_id,
                feedback.expected_result,
                feedback.actual_result
            )
        
        return {"status": "feedback_received", "task_id": feedback.task_id}
    except Exception as e:
        logger.error(f"Feedback processing error: {str(e)}")
        return {"status": "error", "message": str(e)}