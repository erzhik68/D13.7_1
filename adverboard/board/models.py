from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    poster = models.ImageField("Постер", upload_to="ad_image/poster/%Y/%m/%d", blank=True) # '%Y' - четырехзначный год, '%m' - двузначный месяц, а '% d' - двузначный день
    text = models.TextField()
    video = EmbedVideoField(blank=True)

    def get_absolute_url(self):
        return reverse('ad_detail', args=[self.id])

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    photo = models.ImageField("Изображение", upload_to="ad_image/%Y/%m/%d",
                              blank=True)  # '%Y' - четырехзначный год, '%m' - двузначный месяц, а '% d' - двузначный день


class Comment(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    email = models.EmailField(default='user@example.com')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.author} - {self.ad}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


#  python manage.py shell_plus --print-sql