from app.utils.exceptions import INTERNAL_ERROR
import os
import httpx 

async def send_push_notification_service(notification_info):
  token = notification_info.token
  message = notification_info.message
  url = "https://exp.host/--/api/v2/push/send"
  headers = {"Content-Type": "application/json"}
  payload = {
      "to": token,
      "title": "hello",
      "body": message
  }

  async with httpx.AsyncClient() as client:
    response = await client.post(url, json=payload, headers=headers)
    
  try:
      response_data = response.json()
      print(response)
  except ValueError:
      response_data = {"error": "Invalid JSON response from server"}

  return {
      "status_code": response.status_code,
      "response_body": response_data,
      "headers": dict(response.headers)
  }

