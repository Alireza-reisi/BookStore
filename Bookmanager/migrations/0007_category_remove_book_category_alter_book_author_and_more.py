# Generated by Django 5.1.4 on 2025-01-04 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bookmanager', '0006_alter_book_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=100, verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='book',
            name='available',
            field=models.BooleanField(default=True, verbose_name='موجود'),
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(null=True, upload_to='files/books/', verbose_name='فایل'),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default='books/default.jpg', upload_to='books/', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(verbose_name='تاریخ انتشار'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100, verbose_name='عنوان'),
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='books', to='Bookmanager.category', verbose_name='دسته\u200cبندی\u200cها'),
        ),
    ]
