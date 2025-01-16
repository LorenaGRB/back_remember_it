from datetime import date
from bson import ObjectId


user_model = {
    "id": ObjectId,
    "username": str,
    "pwd": str,
    "email": str,
    "fullname": str,
    "mobile_tkn": str,
    "words": [
        {
            "name": str,
            "context": str,
            "is_active": bool,
            "sentences": [
                {"sentence": str, "notification_planned_date": date, "notification_sent": bool}
            ],
        }
    ],
}