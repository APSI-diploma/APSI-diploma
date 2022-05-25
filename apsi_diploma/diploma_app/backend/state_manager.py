from enum import IntEnum
import random

from ..models import User


class StudentState(IntEnum):
    ADD_TITLE = 1
    WAIT_FOR_TITLE_ACCEPT = 2
    SEND_PAPER = 3
    WAIT_FOR_PAPER_ACCEPT = 4


class UserType(IntEnum):
    STUDENT = 1
    PROMOTER = 2


class StateManager:
    def get_student_state(username: str):
        return StudentState(User.objects.filter(username=username)[0].state)

    def get_user_type(username: str):
        return UserType(User.objects.filter(username=username)[0].user_type)

    def update_state(username: str, state=None):
        user = User.objects.get(username=username)
        if state is None:
            user_state = StateManager.get_student_state(username)
            User.objects.filter(username=username).update(state=int(user_state) + 1)
        else:
            User.objects.filter(username=username).update(state=int(state))

    def add_user(username: str):
        if not username in User.objects.values_list("username", flat=True):
            if "PRO" in username:
                user = User.objects.create(username=username, user_type=2, state=1)
            else:
                user = User.objects.create(username=username, user_type=1, state=1)
