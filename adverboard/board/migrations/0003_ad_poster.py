# Generated by Django 4.1.2 on 2022-10-27 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_rename_post_image_ad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='poster',
            field=models.ImageField(blank=True, upload_to='ad_image/poster/%Y/%m/%d', verbose_name='Изображение'),
        ),
    ]