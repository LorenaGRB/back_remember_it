from fastapi import APIRouter, Depends
from app.external_services.push_notification.push_notification_service import send_push_notification_service
from app.schemas.push_notification import push_notification_input
from app.middlewares.auth import AuthenticationMiddleware

router = APIRouter()
auth  = AuthenticationMiddleware()

@router.post("/send", dependencies = [Depends(auth)])
async def send_notification(notification_info: push_notification_input):
  return await send_push_notification_service(notification_info)

# @router.post("/send_all", dependencies = [Depends(auth)])
# async def send_all_notifications():
#   return await send_all_push_notification_service(notification_info)