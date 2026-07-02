import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'remichain.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Matching engine tuning
    URGENCY_WEIGHT = 3.0
    EXPIRY_WEIGHT = 2.0
    PROXIMITY_WEIGHT = 1.5
    QUANTITY_WEIGHT = 1.0
