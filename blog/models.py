from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique_for_date="publish_date")
    body = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["-publish_date"]

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail",
                       kwargs={"slug": self.slug, "year": self.publish_date.year, "month": self.publish_date.month,
                               "day": self.publish_date.day})


class Comment(models.Model):
    author = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    email = models.EmailField()
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author} on post {self.post}"

    class Meta:
        ordering = ["create_date"]
