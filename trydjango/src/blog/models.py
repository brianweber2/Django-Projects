from django.db import models
from django.urls import reverse


class Article(models.Model):
  title = models.CharField(max_length=120)
  content = models.TextField()
  author = models.CharField(max_length=120)
  active = models.BooleanField(default=True)

  def get_absolute_url(self):
    return reverse('articles:article-detail', kwargs={'id': self.id})
