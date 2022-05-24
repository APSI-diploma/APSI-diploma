from ..models import Paper


class Creation:
    username: str

    def __init__(self, username: str):
        self.username = username

    def getPromoterUsername(self, promoter_name: str):
        return ""

    def create_theme(self, promoter: str, title: str):
        Paper.objects.create(
            promoter_username=self.getPromoterUsername(promoter_name=promoter),
            author_username=self.username,
            title=title,
        )
        # print(Paper.objects.values_list("title", flat=True))
