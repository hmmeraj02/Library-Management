# Generated by Django 5.0 on 2024-01-16 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='images',
            field=models.ImageField(upload_to='book/media/uploads/'),
        ),
    ]
