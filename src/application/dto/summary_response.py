from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):
    """Represents a user with personal details such as id, username, first name, last name, email, password, phone, and user status."""

    tittle: str = Field(
        ..., description="News title", example="Rosneft announced dividend payment"
    )
    text: str = Field(
        ...,
        description="News text",
        example="A robotic dog with a rabbit and a minigun is a new word in home security. A Chinese enthusiast has created an unusual hybrid, where a cute animal has become part of the combat system. Now this mecha-hare not only looks threatening, but also effectively performs its task, monitoring the yard.",
    )
