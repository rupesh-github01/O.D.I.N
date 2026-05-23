from pydantic import BaseModel


class GraphQuery(BaseModel):

    concept: str