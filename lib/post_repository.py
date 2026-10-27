from lib.post import Post

class PostRepository:
    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all posts
    def all(self):
        rows = self._connection.execute('SELECT * from posts')
        posts = []
        for row in rows:
            item = Post(row["title"], row["content"], row["tags"], row["id"])
            posts.append(item)
        return posts

    # Find a single post by its id
    def find(self, post_id):
        rows = self._connection.execute(
            'SELECT * from posts WHERE id = %s', [post_id])
        row = rows[0]
        return Post(row["title"], row["content"], row['tags'], row["id"])

    # Create a new post
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, post):
        self._connection.execute('INSERT INTO posts (title, content, tags) VALUES (%s, %s, %s)', [
                                 post.title, post.content, post.tags])
        return None

    # Delete a post by its id
    def delete(self, post_id):
        self._connection.execute(
            'DELETE FROM posts WHERE id = %s', [post_id])
        return None
