import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost/pawnshop_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join("app", "static", "uploads", "items")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    MAX_IMAGES_PER_ITEM = 5
    DEFAULT_INTEREST_RATE = 3.0
    ITEMS_PER_PAGE = 20
    MAX_EXTENSIONS_PER_TICKET = 5
    VIETQR_BANK = "techcombank"
    VIETQR_ACCOUNT = "19073152287011"
    VIETQR_ACCOUNT_NAME = "LE NGOC BAO TRAN"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

