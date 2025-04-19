from piccolo.table import Table
from piccolo.columns import BigSerial


class UserDAO(Table):
    id: BigSerial = BigSerial(primary_key=True)
