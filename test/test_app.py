import pytest
from ..lib.post_repository import PostRepository
from ..lib.post import Post

@pytest.fixture
def post_repository(db_connection):
    return PostRepository(db_connection)

def test_index_route_returns_blog_page(web_client, db_connection):
    db_connection.seed("seeds/posts.sql")
    response = web_client.get('/')
    assert response.status_code == 200
    assert b'The Working Blog' in response.data

def test_create_post_redirects_to_home(web_client, db_connection):
    db_connection.seed("seeds/posts.sql")
    response = web_client.post('/posts', data={
        'title': 'Test Post',
        'content': 'Test Content',
        'tags': 'tag1,tag2'
    })
    assert response.status_code == 302

def test_posts_by_tag_route_renders_template(web_client, post_repository, db_connection):
    db_connection.seed("seeds/posts.sql")
    # Given a post exists
    post = Post("Python Tutorial", "Learn Python", ["python"])
    post_repository.create(post)
    
    # When requesting posts by tag
    response = web_client.get('/tag/python')
    
    # Then the page renders successfully
    assert response.status_code == 200

def test_form_submission_creates_post_in_manager(web_client, post_repository, db_connection):
    db_connection.seed("seeds/posts.sql")
    # When submitting a new post
    web_client.post('/posts', data={
        'title': 'Integration Test Post',
        'content': 'This is test content',
        'tags': 'test,integration'
    })
    
    # Then the post is added to the manager
    posts = post_repository.all()
    assert len(posts) == 6
    assert posts[5].title == 'Integration Test Post'
