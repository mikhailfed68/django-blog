from blog.models import Blog, Article, Language


def create_test_blog(name, description='testing'):
    """
    Creates blog with 'test' fields.
    'name' argument is identifier added to
    name to provide unique constraints.
    """
    return Blog.objects.create(name=name, description=description)


def create_test_language(language):
    """
    Creates language with 'test' fields.
    'name' argument is identifier added to
    name to provide unique constraints.
    """
    return Language.objects.create(language=language)


def create_test_article(name, author):
    """
    Creates article with 'test' fields.
    'name' argument is identifier added to
    name to provide unique constraints.
    """
    language, is_created = Language.objects.get_or_create(language='Testing')
    return Article.objects.create(
        title=name,
        description=name,
        body=name,
        author=author,
        language=language,
    )
