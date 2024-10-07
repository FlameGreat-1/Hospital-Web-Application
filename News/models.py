from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    video = models.FileField(upload_to='news_videos/', blank=True, null=True)
    publication_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title
