from django.urls import path
from . import views


app_name = 'Profile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('add-book/', views.add_book, name='add-book'),
    path('mybooks/', views.my_books, name='my-books'),
    path('favorites/', views.my_favorites, name='favorites'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete-book'),
    path('edit-book/<slug:slug>/', views.edit_book, name='edit-book'),
]
