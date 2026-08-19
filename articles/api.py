from ninja import Router
from articles.models import Article, Category
from articles.schemas import ArticleCreateSchema, ArticleUpdateSchema, ArticleOutSchema
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.post("/", response={201: ArticleOutSchema, 400: dict})
def create_article(request, data: ArticleCreateSchema):
    user = request.auth
    category = None
    if data.category_id:
        category = get_object_or_404(Category, id=data.category_id)
    article = Article.objects.create(
        title=data.title, content=data.content, author=user, category=category
    )
    logger.info(f"Article created: {article.id} by {user.username}")
    return 201, ArticleOutSchema.from_orm(article)


@router.get("/", response=list[ArticleOutSchema])
def list_articles(request):
    articles = Article.objects.all().select_related("author", "category")
    return articles


@router.get("/{int:article_id}", response=ArticleOutSchema)
def get_article(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    return article


@router.put("/{int:article_id}", response={200: ArticleOutSchema, 403: dict, 404: dict})
def update_article(request, article_id: int, data: ArticleUpdateSchema):
    article = get_object_or_404(Article, id=article_id)
    if article.author != request.auth:
        logger.warning(
            f"Unauthorized edit attempt on article {article_id} by {request.auth.username}"
        )
        return 403, {"error": "You are not the author"}
    if data.title is not None:
        article.title = data.title
    if data.content is not None:
        article.content = data.content
    if data.category_id is not None:
        article.category = get_object_or_404(Category, id=data.category_id)
    article.save()
    logger.info(f"Article {article_id} updated by {request.auth.username}")
    return article


@router.delete("/{int:article_id}", response={200: dict, 403: dict, 404: dict})
def delete_article(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    if article.author != request.auth:
        return 403, {"error": "Not your article"}
    article.delete()
    logger.info(f"Article {article_id} deleted by {request.auth.username}")
    return {"success": True}
