# id like to use fastapi 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime


app = FastAPI()

origins = [
    "http://localhost:56409",  # Your Flutter app's origin
    "http://localhost:8888", # The local host of the API
    "http://localhost:61785",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the SQLAlchemy Base and Session
Base = declarative_base()
engine = create_engine('sqlite:///./test.sqlite')  # Use your own database URL here
Session = sessionmaker(bind=engine)

# Define the SQLAlchemy model
class Dream(Base):
    __tablename__ = "dreams"

    db_id = Column(String, primary_key=True)
    user_id = Column(String)
    date = Column(String)
    dream = Column(String)

# Create the table
Base.metadata.create_all(bind=engine)

# Define the Pydantic model
class DreamModel(BaseModel):
    user_id: str
    dream: str


class TextModel(BaseModel):
    text: str












@app.post("/reverse")
def reverse_text(body: TextModel):
    # take input text and return it reversed
    return {"reversed_text": body.text[::-1]}





@app.post("/dream")
def create_dream(dream: DreamModel):
    # Create a new SQLAlchemy session
    session = Session()

    # get counts of dreams
    count = session.query(Dream).count()

    date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M")

    # Create a new Dream object
    new_dream = Dream(db_id=count + 1, user_id=dream.user_id, date=date, dream=dream.dream)

    # Add the new dream to the session and commit it
    session.add(new_dream)
    session.commit()

    # Close the session
    session.close()

    return {"message": "Dream created successfully"}


@app.get("/dreams/{requested_user_id}")
def get_dreams(requested_user_id: str): 
    # Create a new SQLAlchemy session
    session = Session()

    # Query dreams for the requested user_id
    dreams = session.query(Dream.date, Dream.dream).filter(Dream.user_id == requested_user_id).all()

    # Close the session
    session.close()

    dreams = [{"date": dream[0], "dream": dream[1]} for dream in dreams]

    # Return the dreams
    return {"dreams": dreams}






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)