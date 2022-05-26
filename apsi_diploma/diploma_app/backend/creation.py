from .user_manager import UserManager
from ..models import Paper, User


class Creation:
    username: str

    def __init__(self, username: str):
        self.username = username

    def create_theme(self, promoter: str, title: str):
        Paper.objects.create(
            promoter_username=UserManager.getPromoterUsername(promoter_name=promoter),
            author_username=self.username,
            title=title,
        )
        # print(Paper.objects.values_list("title", flat=True))
