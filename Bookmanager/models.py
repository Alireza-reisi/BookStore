import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to='img/categories', null=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=50, null=False, blank=False, unique=True)

    def get_absolute_url(self):
        return reverse('Bookmanager:category_page', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.english_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class book(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    english_title = models.CharField(max_length=100, verbose_name="عنوان انگلیسی")
    author = models.CharField(max_length=100, verbose_name="نویسنده")
    published_date = models.DateField(auto_now_add=True, verbose_name="تاریخ انتشار")
    available = models.BooleanField(default=True, verbose_name="موجود")
    image = models.ImageField(upload_to='img/books', null=False,
                              default='assets/img/default.jpg', verbose_name="تصویر")
    file = models.FileField(upload_to='file/books', null=False, verbose_name="فایل",
                            default='assets/file/book.pdf')
    categories = models.ManyToManyField(Category, related_name='books', verbose_name="دسته‌بندی‌ها")
    sell = models.IntegerField(default=0, null=False)
    book_slug = models.SlugField(null=False, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    comment_number = models.IntegerField(default=0, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    translator = models.CharField(max_length=100, verbose_name="مترجم", null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    view = models.IntegerField(default=0, null=False)
    download_number = models.IntegerField(default=0, null=False)

    def get_absolute_url(self):
        return reverse('Bookmanager:book_page', args=[self.book_slug])

    def save(self, *args, **kwargs):
        slug = slugify(self.english_title)
        while True:
            i = 0
            if book.objects.filter(book_slug=slug).exclude(id=self.id).exists():
                i += 1
                slug = slug + str(i)
            else:
                break
        self.book_slug = slug
        super(book, self).save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    book = models.ForeignKey(book, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=200, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.book.title} - {self.author.username} - {self.id}"

