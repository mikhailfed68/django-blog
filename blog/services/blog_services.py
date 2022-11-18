from blog.models import Article


def get_latest_created_articles():
    return Article.objects.order_by('-created_at')[:10]
