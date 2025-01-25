from django.http import Http404, FileResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from .models import Category, book, Comment
from django.db.models import Count, Q
import os


def index(request):
    categories = Category.objects.all()
    books = book.objects.all()
    most_view_books = book.objects.order_by('-view')[:10]
    most_download_books = book.objects.order_by('-download_number')[:10]
    last_books = book.objects.order_by('-published_date')[:6]
    last_Sport_books = book.objects.filter(categories__name="ورزش و تندرستی").distinct().order_by('-published_date')[:6]
    last_Historical_books = book.objects.filter(categories__name="تاریخی").distinct().order_by('-published_date')[:6]
    last_Business_books = book.objects.filter(categories__name="کسب و کار").distinct().order_by('-published_date')[:6]
    last_Stories_books = book.objects.filter(categories__name="داستان و رمان").distinct().order_by('-published_date')[
                         :6]
    publishers_data = book.objects.values('publisher').annotate(book_count=Count('publisher')).order_by('-book_count')[
                      :8]

    return render(request, 'index.html',
                  {'books': books, 'categories': categories, 'most_view_books': most_view_books,
                   'most_download_books': most_download_books, 'last_books': last_books,
                   'last_Sport_books': last_Sport_books, 'last_Historical_books': last_Historical_books,
                   'last_Business_books': last_Business_books, 'last_Stories_books': last_Stories_books,
                   'publishers': publishers_data, })


def Category_page(request, slug):
    if Category.objects.filter(slug=slug).exists():
        category = Category.objects.get(slug=slug)
        books = book.objects.filter(categories=category)
        return render(request, 'categories.html', {'category': category, 'books': books})
    else:
        return redirect('Bookmanager:home')


def Book_page(request, slug):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if book.objects.filter(book_slug=slug).exists():
                text = request.POST.get('comment')
                this_book = book.objects.get(book_slug=slug)
                this_book.comment_number += 1
                this_book.save()
                Comment.objects.create(text=text, author=request.user, book=this_book)
                return redirect(reverse('Bookmanager:book_page', args=[this_book.book_slug]))
            else:
                return redirect('Bookmanager:home')
        else:
            return redirect('users:login')
    elif request.method == 'GET':
        if book.objects.filter(book_slug=slug).exists():
            this_book = book.objects.get(book_slug=slug)
            this_book.view += 1
            this_book.save()
            this_book_category = this_book.categories.all()
            this_book_comments = this_book.comments.all()
            related_books = book.objects.filter(categories__in=this_book_category).exclude(id=this_book.id).distinct()
            return render(request, 'book-details.html',
                          {'this_book': this_book, 'this_book_category': this_book_category,
                           'this_book_comments': this_book_comments,
                           'related_books': related_books})
        else:
            return redirect('Bookmanager:home')


def book_search(request):
    query = request.GET.get('query', '')
    if query:
        books = book.objects.filter(Q(author__icontains=query) | Q(title__icontains=query) |
                                    Q(publisher__icontains=query) | Q(categories__name__icontains=query)).distinct()
    else:
        books = []

    context = {
        'query': query,
        'books': books,
    }
    return render(request, 'search.html', context)


def all_books(request):
    books = book.objects.all()
    return render(request, 'all_books.html', {'books': books})


def download_book(request, slug):
    if book.objects.filter(book_slug=slug).exists():
        this_book = book.objects.get(book_slug=slug)
        file_path = this_book.file.path

        if not os.path.exists(file_path):
            raise Http404("کتاب مورد نظر یافت نشد.")

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        raise Http404("کتاب مورد نظر یافت نشد.")
