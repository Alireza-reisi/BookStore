from django.urls import path
from . import views

app_name = 'Bookmanager'
urlpatterns = [
    path('', views.index, name='home'),
    path('category/<slug:slug>', views.Category_page, name='category_page'),
    path('book/<slug:slug>', views.Book_page, name='book_page'),
    path('search/', views.book_search, name='book_search'),
    path('all-books', views.all_books, name='all_books'),
    path('download/<slug:slug>', views.download_book, name='download_book' )
]
