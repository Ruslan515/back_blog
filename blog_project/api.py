from ninja import NinjaAPI
from users.api import router as users_router
from articles.api import router as articles_router
from comments.api import router as comments_router
from ninja.security import HttpBearer
from users.models import User


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user = User.objects.get(token=token)
            return user
        except User.DoesNotExist:
            return None


api = NinjaAPI(auth=AuthBearer())

api.add_router("/users", users_router)
api.add_router("/articles", articles_router)
api.add_router("/comments", comments_router)
