from datetime import datetime
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
            "creation_date": datetime,
            "sentences": [
                {"sentence": str, "date": datetime}
            ],
        }
    ],
}