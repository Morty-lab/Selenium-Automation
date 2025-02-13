class Video:
    def __init__(self, video_id, title, description, views, likes, dislikes):
        self.video_id = video_id
        self.title = title
        self.description = description
        self.views = views
        self.likes = likes
        self.dislikes = dislikes

    def get_video_id(self):
        return self.video_id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_views(self):
        return self.views

    def get_likes(self):
        return self.likes

    def get_dislikes(self):
        return self.dislikes

    def set_video_id(self, video_id):
        self.video_id = video_id

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_views(self, views):
        self.views = views

    def set_likes(self, likes):
        self.likes = likes

    def set_dislikes(self, dislikes):
        self.dislikes = dislikes

