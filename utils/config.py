from dotenv import load_dotenv
import os




def configure():
    load_dotenv()



class Config:
    configure()
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    # SECRET_KEY = "f59601b41eb1dadf1baeef3c837fb445"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///flaskap.db"


    