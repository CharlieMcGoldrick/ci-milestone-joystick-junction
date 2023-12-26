from django.db import models
from django.contrib.auth.models import User

# Model Status
STATUS = ((0, "Draft"), (1, "Published"))

class MainThread(models.Model):
    game_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    cover = models.URLField(blank=True, null=True)
    first_release_date = models.DateTimeField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    platforms = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    artwork = models.URLField(blank=True, null=True)
    age_ratings = models.TextField(blank=True, null=True)
    involved_companies = models.TextField(blank=True, null=True)
    game_engines = models.TextField(blank=True, null=True)
    aggregated_rating = models.FloatField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # on_delete=models.CASCADE means if the user is deleted,
    # their blog posts will be deleted too
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    # featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User,
        related_name='blog_likes',
        blank=True
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
