from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from datetime import datetime
import json

# Model Status
STATUS = ((0, "Draft"), (1, "Published"))

class MainThread(models.Model):
    game_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    genres = models.TextField(blank=True, null=True)
    platforms = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    involved_companies = models.TextField(blank=True, null=True)
    game_engines = models.TextField(blank=True, null=True)
    aggregated_rating = models.FloatField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def set_genres(self, genres):
        self.genres = json.dumps(genres)

    def get_genres(self):
        return json.loads(self.genres)

    def set_platforms(self, platforms):
        self.platforms = json.dumps(platforms)

    def get_platforms(self):
        return json.loads(self.platforms)

    def set_involved_companies(self, involved_companies):
        self.involved_companies = json.dumps(involved_companies)

    def get_involved_companies(self):
        return json.loads(self.involved_companies)

    def set_game_engines(self, game_engines):
        self.game_engines = json.dumps(game_engines)

    def get_game_engines(self):
        return json.loads(self.game_engines)

    # Add new fields for visibility state
    name_visible = models.BooleanField(default=True)
    summary_visible = models.BooleanField(default=True)
    genres_visible = models.BooleanField(default=False)
    platforms_visible = models.BooleanField(default=False)
    involved_companies_visible = models.BooleanField(default=False)
    game_engines_visible = models.BooleanField(default=False)
    aggregated_rating_visible = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Comment(models.Model):
    game_id = models.ForeignKey(MainThread, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',  null=True)
    text = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField('Upvote', blank=True, related_name='comments_upvoted')
    downvotes = models.ManyToManyField('Downvote', blank=True, related_name='comments_downvoted')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.text

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='upvotes_from')

    def __str__(self):
        return f'Upvote by {self.user} on {self.comment}'

class Downvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='downvotes_from')

    def __str__(self):
        return f'Downvote by {self.user} on {self.comment}'