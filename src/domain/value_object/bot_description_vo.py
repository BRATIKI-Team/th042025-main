class BotDescriptionVO:
    def __init__(self, description: str):
        self._description = description
        self._validate()

    def _validate(self) -> None:
        if len(self._description) > 1023:
            raise ValueError("Description must be less than 1023 characters")

    @property
    def description(self) -> str:
        return self._description
