from piccolo.table import Table
from piccolo.columns import BigSerial


class UserDAO(Table):
    id: int = BigSerial(primary_key=True)
