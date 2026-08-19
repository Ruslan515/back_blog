from ninja import Router
from django.shortcuts import get_object_or_404
from comments.models import Comment
from comments.schemas import CommentCreateSchema, CommentUpdateSchema, CommentOutSchema
from articles.models import Article
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.post("/", response={201: CommentOutSchema, 400: dict, 403: dict, 404: dict})
def create_comment(request, data: CommentCreateSchema):
    user = request.auth
    article = get_object_or_404(Article, id=data.article_id)
    comment = Comment.objects.create(author=user, article=article, text=data.text)
    logger.info(
        f"Comment {comment.id} created by {user.username} on article {article.id}"
    )
    return 201, CommentOutSchema.from_orm(comment)


@router.get("/", response=list[CommentOutSchema])
def list_comments(request, article_id: int = None):
    # Можно фильтровать по статье, если передан параметр
    queryset = Comment.objects.all().select_related("author", "article")
    if article_id:
        queryset = queryset.filter(article_id=article_id)
    return queryset


@router.get("/{int:comment_id}", response=CommentOutSchema)
def get_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    return comment


@router.put("/{int:comment_id}", response={200: CommentOutSchema, 403: dict, 404: dict})
def update_comment(request, comment_id: int, data: CommentUpdateSchema):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.auth:
        logger.warning(
            f"Unauthorized edit attempt on comment {comment_id} by {request.auth.username}"
        )
        return 403, {"error": "You are not the author of this comment"}
    comment.text = data.text
    comment.save()
    logger.info(f"Comment {comment_id} updated by {request.auth.username}")
    return comment


@router.delete("/{int:comment_id}", response={200: dict, 403: dict, 404: dict})
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.auth:
        logger.warning(
            f"Unauthorized delete attempt on comment {comment_id} by {request.auth.username}"
        )
        return 403, {"error": "Not your comment"}
    comment.delete()
    logger.info(f"Comment {comment_id} deleted by {request.auth.username}")
    return {"success": True}
