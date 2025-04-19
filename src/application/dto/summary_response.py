from pydantic import BaseModel

class SummaryResponse(BaseModel):
    """Represents a user with personal details such as id, username, first name, last name, email, password, phone, and user status."""
    tittle: str = Field(..., description="Заголовок новости", example="Роснефть объявила о выплате дивидендов")
    text: str = Field(..., description="Текст нговости", example="Робособака с кроликом и миниганом — новое слово в домашней охране. Китайский энтузиаст создал необычный гибрид, где милый зверёк стал частью боевой системы. Теперь этот меха-заяц не только выглядит угрожающе, но и эффективно выполняет свою задачу, контролируя двор.")
