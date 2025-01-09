from backend.dao import base
from backend.users import models


class UsersDAO(base.BaseDAO[models.Users]):
    model = models.Users
