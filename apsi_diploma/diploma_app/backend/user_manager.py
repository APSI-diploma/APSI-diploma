from enum import IntEnum
import random

from ..models import User, Paper


class StudentState(IntEnum):
    ADD_TITLE = 1
    WAIT_FOR_TITLE_ACCEPT = 2
    SEND_PAPER = 3
    WAIT_FOR_PAPER_ACCEPT = 4


class UserType(IntEnum):
    STUDENT = 1
    PROMOTER = 2


class UserManager:
    # zwraca Stan dyplomowania w którym znajduje się student
    def get_student_state(username: str):
        return StudentState(User.objects.filter(username=username)[0].state)

    # zwraca typ użytkownika
    def get_user_type(username: str):
        return UserType(User.objects.filter(username=username)[0].user_type)

    # zmienia stan użytkownika na następny (jeśli state=None) lub na konkretny inny stan
    def update_state(username: str, state=None):
        user = User.objects.get(username=username)
        if state is None:
            user_state = UserManager.get_student_state(username)
            User.objects.filter(username=username).update(state=int(user_state) + 1)
        else:
            User.objects.filter(username=username).update(state=int(state))

    # dodaje użytkownika do bazy
    def add_user(username: str):
        if not username in User.objects.values_list("username", flat=True):
            if "PRO" in username:
                user = User.objects.create(username=username, user_type=2, state=1)
            else:
                user = User.objects.create(username=username, user_type=1, state=1)

    # zwraca QuerySet objektów User
    def get_list_of_promotores():
        return User.objects.filter(user_type=User.UserType.PROMOTER)

    def getPromoterUsername(self, promoter_name: str):
        users = User.objects.filter(
            name=promoter_name.split(" ")[0],
            surname=promoter_name.split(" ")[1],
            user_type=User.UserType.PROMOTER,
        )
        print(users)
        print(users[0])
        return users[0]["username"]

    def get_pending_titles(promoter_username: str):
        return Paper.objects.filter(
            promoter_username=promoter_username, isAccepted=False
        )

    def accept_title(username: str, title: str):
        Paper.objects.filter(author_username=username, title=title).update(
            isAccepted=True
        )
        user_state = UserManager.get_student_state(username)
        User.objects.filter(username=username, title=title).update(
            state=int(user_state) + 1
        )

    def discard_title(username: str, title: str):
        Paper.objects.filter(author_username=username, title=title).delete()
        user_state = UserManager.get_student_state(username)
        User.objects.filter(username=username, title=title).update(
            state=int(StudentState.ADD_TITLE)
        )

