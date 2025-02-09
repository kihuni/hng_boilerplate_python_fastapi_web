from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.v1.models.user import User
from api.v1.schemas.activity_logs import ActivityLogCreate, ActivityLogResponse
from api.v1.services.activity_logs import activity_log_service
from api.v1.services.user import user_service
from api.db.database import get_db
from api.utils.success_response import success_response

activity_logs = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])


@activity_logs.post("/create", status_code=status.HTTP_201_CREATED)
async def create_activity_log(activity_log: ActivityLogCreate, db: Session = Depends(get_db)):
    '''Create a new activity log'''

    new_activity_log = activity_log_service.create_activity_log(
        db=db,
        user_id=activity_log.user_id,
        action=activity_log.action
    )

    return success_response(
        status_code=201,
        message="Activity log created successfully",
        data=jsonable_encoder(new_activity_log)
    )


@activity_logs.get("/", response_model=list[ActivityLogResponse])
async def get_all_activity_logs(current_user: User = Depends(user_service.get_current_super_admin), db: Session = Depends(get_db)):
    '''Get all activity logs'''

    activity_logs = activity_log_service.get_all_activity_logs(db=db)

    return success_response(
        status_code=200,
        message="Activity logs retrieved successfully",
        data=jsonable_encoder(activity_logs)
    )
