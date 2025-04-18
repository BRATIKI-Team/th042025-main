class BotNameVO:
    def __init__(self, name: str):
        self._name = name
        self._validate()

    def _validate(self) -> None:
        if len(self._name) > 255:
            raise ValueError("Name must be less than 255 characters")

    @property
    def value(self) -> str:
        return self._name
