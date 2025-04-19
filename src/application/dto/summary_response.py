from pydantic import BaseModel

class SummaryResponse(BaseModel):
    """Represents a user with personal details such as id, username, first name, last name, email, password, phone, and user status."""
    tittle: str = Field(..., description="��������� �������", example="�������� �������� � ������� ����������")
    text: str = Field(..., description="����� ��������", example="���������� � �������� � ��������� � ����� ����� � �������� ������. ��������� ��������� ������ ��������� ������, ��� ����� ����� ���� ������ ������ �������. ������ ���� ����-���� �� ������ �������� ���������, �� � ���������� ��������� ���� ������, ����������� ����.")
