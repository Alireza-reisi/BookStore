# Generated by Django 5.1.4 on 2025-01-07 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bookmanager', '0031_alter_book_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='translator',
            field=models.CharField(max_length=100, null=True),
        ),
    ]