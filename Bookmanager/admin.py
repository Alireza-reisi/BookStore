from django.contrib import admin
from .models import book, Category, Comment


admin.site.register(book)
admin.site.register(Category)
admin.site.register(Comment)
