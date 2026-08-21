from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{os.getenv('MYSQL_USER')}:"
        f"{os.getenv('MYSQL_PASSWORD')}@"
        f"{os.getenv('MYSQL_HOST')}:"
        f"{os.getenv('MYSQL_PORT')}/"
        f"{os.getenv('MYSQL_DATABASE')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("SECRET_KEY")

class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:ruphinee@localhost/vms_test_db"
    )


JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "change-this-secret"
)

JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


FRONTEND_BASE_URL = (
    "http://localhost:5173"
)

# Later
# Development: http:localhost:5173
# Production: https://vms.example.com
