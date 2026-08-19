from ninja import Router
from django.contrib.auth import authenticate
from users.models import User
from users.schemas import UserRegisterSchema, UserLoginSchema, UserOutSchema
import secrets
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.post("/register", response={200: UserOutSchema, 400: dict}, auth=None)
def register(request, data: UserRegisterSchema):
    if User.objects.filter(username=data.username).exists():
        return 400, {"error": "Username already taken"}
    user = User.objects.create_user(username=data.username, password=data.password)
    token = secrets.token_urlsafe(256)
    user.token = token
    user.save()
    logger.info(f"New user registered: {user.username}")
    return 200, {"id": user.id, "username": user.username, "token": token}


@router.post("/login", response={200: UserOutSchema, 401: dict}, auth=None)
def login(request, data: UserLoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if user is None:
        logger.warning(f"Failed login attempt for {data.username}")
        return 401, {"error": "Invalid credentials"}
    if not user.token:
        user.token = secrets.token_urlsafe(256)
        user.save()
    logger.info(f"User logged in: {user.username}")
    return 200, {"id": user.id, "username": user.username, "token": user.token}
