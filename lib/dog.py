from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

print("Current working directory:", os.getcwd())

Base = declarative_base()

class Dog(Base):
    __tablename__ = 'dogs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    breed = Column(String)

def create_table(base, engine):
    print("Creating tables...")
    base.metadata.create_all(engine)
    print("Tables created.")

def save(session, dog):
    print(f"Saving dog: name={dog.name}, breed={dog.breed}")
    session.add(dog)
    session.commit()
    print("Dog saved.")

def get_all(session):
    print("Getting all dogs...")
    dogs = session.query(Dog).all()
    print(f"Found {len(dogs)} dogs.")
    return dogs

def find_by_name(session, name):
    print(f"Finding dog by name: {name}")
    dog = session.query(Dog).filter(Dog.name == name).first()
    print(f"Found: {dog}")
    return dog

def find_by_id(session, id):
    print(f"Finding dog by id: {id}")
    dog = session.get(Dog, id)
    print(f"Found: {dog}")
    return dog

def find_by_name_and_breed(session, name, breed):
    print(f"Finding dog by name '{name}' and breed '{breed}'")
    dog = session.query(Dog).filter(Dog.name == name, Dog.breed == breed).first()
    print(f"Found: {dog}")
    return dog

def update_breed(session, dog, breed):
    print(f"Updating dog id={dog.id} breed from {dog.breed} to {breed}")
    dog.breed = breed
    session.commit()
    print("Dog breed updated.")

if __name__ == "__main__":
    # Use absolute path for DB file:
    db_filename = "dog.db"
    db_path = os.path.join(os.getcwd(), db_filename)
    print("Database file path:", db_path)

    engine = create_engine(f'sqlite:///{db_path}', echo=True)
    create_table(Base, engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    dog1 = Dog(name="Buddy", breed="Golden Retriever")
    save(session, dog1)

    all_dogs = get_all(session)
    print("All dogs:", all_dogs)

    dog_by_name = find_by_name(session, "Buddy")
    dog_by_id = find_by_id(session, dog1.id)
    dog_by_name_breed = find_by_name_and_breed(session, "Buddy", "Golden Retriever")
    update_breed(session, dog1, "Labrador Retriever")

    updated_dog = find_by_id(session, dog1.id)
    print("Updated dog:", updated_dog)

    # Confirm DB file exists
    if os.path.exists(db_path):
        print(f"Database file successfully created at: {db_path}")
    else:
        print("Database file NOT found!")
