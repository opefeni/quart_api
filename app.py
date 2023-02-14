#import libraries
from quart import g, Quart
from quart_db import QuartDB
from quart_schema import QuartSchema, validate_request, validate_response
from dataclasses import dataclass

# instantiate objects
app =  Quart(__name__)
QuartDB(app, url="sqlite:///database.db")
QuartSchema(app)

# create a dataclass for the db field
@dataclass
class CardInput:
    question: str   
    answer: str

@dataclass
class Card:
    id: int
    question: str
    answer: str


@app.post("/cards/")
@validate_request(CardInput)
@validate_response(Card)
async def create_card(data: CardInput) -> Card:
    """ Create a new Anki Card"""

    result = await g.connection.fetch_one(
        """ INSERT INTO cards (question, answer)
               VALUES(:question, :answer)
               RETURNING id, question, answer""",
             {"question": data.question, "answer": data.answer}
    )
    # unpack the result using ** 
    return Card(**result)

# @app.get("/")
# async def index():
#     return {"Hello": "World"}

if __name__ == '__main__':
     app.run()