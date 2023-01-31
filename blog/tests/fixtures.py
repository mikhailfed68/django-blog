from blog.models import Blog, Article, Language


def create_test_blog(name, description='testing'):
    """
    Creates blog with 'test' fields.
    'name' argument is identifier added to
    name to provide unique constraints.
    """
    return Blog.objects.create(name=f'test_{name}', description=description)


def create_test_language(language):
    """
    Creates language with 'test' fields.
    'name' argument is identifier added to
    name to provide unique constraints.
    """
    return Language.objects.create(language=f'test_{language}')


def create_test_article(name, author):
    """
    Creates article with 'test' fields.
    'name' argument is identifier added to
    name to provide unique constraints.
    """
    return Article.objects.create(
        title=f'test_{name}',
        description=f'test_{name}',
        body=f'test_{name}',
        author=author,
        language=create_test_language(1)
    )
