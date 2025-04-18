from pydantic import BaseModel


class SummaryRequest(BaseModel):
    title: str
    summary: str
