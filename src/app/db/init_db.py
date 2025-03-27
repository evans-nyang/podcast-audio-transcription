from .database import engine, Base

def init_db():
    """Creates database tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized.")
