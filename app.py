#import libraries
from quart import g, Quart, abort
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

@dataclass
class Cards:
    cards: list([[Card]]) 

#  Endpoint to get all the rows
@app.get("/cards/")
#@validate_response(Cards)
async def get_cards() -> Cards:
    query =  """ SELECT id, question, answer FROM cards"""
    
    cards = [Card(**row) 
    async for row in g.connection.iterate(query)
    ]

    return cards

@app.put("/cards/<int:id>/")
@validate_response(Card)
@validate_request(CardInput)
async def update_card(id:int, data:CardInput)->Card:
    result = await g.connection.fetch_one(
        """ UPDATE cards set
                    question=:question, answer=:answer
            WHERE id=:id
            RETURNING id, question, answer
        """, {"id": id, "question": data.question, "answer": data.answer },
    )
    if result is None:
        abort(404)
    return Card(**result)

@app.delete("/cards/<int:id>")
async def delete_card(id:int)->str:
    await g.connection.execute(
        "DELETE from cards WHERE id= :id",
        {"id": id},
    )
    return "DELETED"


#@app.get("/")
# async def index():
#     return {"Hello": "World"}

if __name__ == '__main__':
     app.run()