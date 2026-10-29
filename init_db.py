from backend.database import Base, engine
from backend.models import Document
from backend.users import User

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")