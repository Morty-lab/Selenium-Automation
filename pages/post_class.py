class Post:
    def __init__(self, post_id, author, text, comments, likes, shares):
        self.post_id = post_id
        self.author = author
        self.text = text
        self.comments = comments
        self.likes = likes
        self.shares = shares

    def get_post_id(self):
        return self.post_id

    def get_author(self):
        return self.author

    def get_text(self):
        return self.text

    def get_comments(self):
        return self.comments

    def get_likes(self):
        return self.likes

    def get_shares(self):
        return self.shares

    def set_post_id(self, post_id):
        self.post_id = post_id

    def set_author(self, author):
        self.author = author

    def set_text(self, text):
        self.text = text

    def set_comments(self, comments):
        self.comments = comments

    def set_likes(self, likes):
        self.likes = likes

    def set_shares(self, shares):
        self.shares = shares

