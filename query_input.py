"""A place designed to accommodate the user's request body (/query)."""
from pydantic import BaseModel

class QueryInput(BaseModel):
    """Class to accommodate the user's request body."""
    prompt:str