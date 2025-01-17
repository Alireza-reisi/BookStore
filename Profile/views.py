from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from Bookmanager.models import Category, book
from Profile.forms import BookForm
from django.http import JsonResponse


def add_book(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if book.objects.filter(title=request.POST.get('title')).exists():
                messages.error(request, 'کتابی با این عنوان از قبل وجود دارد')
                return redirect('Profile:add-book')
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                new_book = form.save(commit=False)
                new_book.creator = request.user  # کتاب به کاربر وارد شده اختصاص پیدا می‌کند
                new_book.save()
                form.save_m2m()  # ذخیره دسته‌بندی‌های چند به چند
                return redirect('Profile:my-books')  # بازگشت به صفحه اصلی
        else:
            form = BookForm()
        categories = Category.objects.all()
        return render(request, 'add_book.html', {'form': form, 'categories': categories})
    else:
        return redirect('Bookmanager:home')


def delete_book(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            deleted_book = book.objects.get(pk=pk)
            try:
                deleted_book.delete()
                messages.success(request, 'کتاب با موفقیت حذف شد.')
                return redirect('Profile:my-books')
            except deleted_book.DoesNotExist:
                messages.error(request, 'کتاب مورد نظر یافت نشد.')
                return redirect('Profile:my-books')
        return JsonResponse({'status': 'error', 'message': 'روش درخواست اشتباه است'})
    else:
        return redirect('Bookmanager:home')


def my_books(request):
    if request.user.is_authenticated:
        mybooks = book.objects.filter(creator=request.user)
        return render(request, 'my_books.html', {'mybooks': mybooks})
    else:
        return redirect('Bookmanager:home')


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # بررسی نام کاربری تکراری
            if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                # ارسال خطای خاص نام کاربری تکراری
                return render(request, 'profile.html', {
                    'error_username': "نام کاربری قبلاً استفاده شده است. لطفاً یک نام کاربری دیگر وارد کنید.",
                    'user': request.user
                })

            # اعتبارسنجی پسوردها
            if new_password and new_password != confirm_password:
                messages.error(request, "رمز عبور جدید و تایید آن مطابقت ندارند.")
                return redirect('Profile:profile')

            # ذخیره تغییرات
            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            # اگر پسورد جدید وارد شده باشد، آن را ذخیره کن
            if new_password:
                user.set_password(new_password)

            user.save()
            messages.success(request, "تغییرات با موفقیت ذخیره شد.")
            return redirect('Profile:profile')

        return render(request, 'profile.html', {'user': request.user})
    else:
        return redirect('Bookmanager:home')


def my_favorites(request):
    if request.user.is_authenticated:
        return render(request, 'my_favorites.html')
    else:
        return redirect('Bookmanager:home')


def edit_book(request, slug):
    if not request.user.is_authenticated:
        return redirect('Bookmanager:home')  # بازگشت به صفحه خانه برای کاربران غیر وارد شده
    else:
        if book.objects.filter(book_slug=slug).exists():
            this_book = book.objects.get(book_slug=slug)

            if request.method == 'POST':
                # دریافت اطلاعات از فرم
                title = request.POST.get('title')
                english_title = request.POST.get('english_title')
                author = request.POST.get('author')
                translator = request.POST.get('translator')
                publisher = request.POST.get('publisher')
                description = request.POST.get('description')
                categories = request.POST.getlist('categories')
                image = request.FILES.get('image')
                file = request.FILES.get('file')

                # اعتبارسنجی و ذخیره تغییرات در صورت لزوم
                updated = False

                if title and title != this_book.title:
                    if not book.objects.filter(title=title).exists():
                        this_book.title = title
                        updated = True

                if english_title and english_title != this_book.english_title:
                    if not Book.objects.filter(english_title=english_title).exists():
                        this_book.english_title = english_title
                        updated = True

                if author and author != this_book.author:
                    this_book.author = author
                    updated = True

                if translator and translator != this_book.translator:
                    this_book.translator = translator
                    updated = True

                if publisher and publisher != this_book.publisher:
                    this_book.publisher = publisher
                    updated = True

                if description and description != this_book.description:
                    this_book.description = description
                    updated = True

                if image:
                    this_book.image = image
                    updated = True

                if file:
                    this_book.file = file
                    updated = True

                if categories:
                    category_objects = Category.objects.filter(id__in=categories)
                    if set(category_objects) != set(this_book.categories.all()):
                        this_book.categories.set(category_objects)
                        updated = True

                # ذخیره تغییرات در صورت وجود
                if updated:
                    this_book.save()
                    messages.success(request, 'کتاب با موفقیت ویرایش شد.')
                else:
                    messages.info(request, 'تغییری برای ذخیره وجود نداشت.')

                return redirect('Profile:my-books')

            elif request.method == 'GET':
                # بارگذاری دسته‌بندی‌ها برای فیلد انتخاب
                categories = Category.objects.all()
                return render(request, 'edit_book.html', {'this_book': this_book, 'categories': categories})
        else:
            return redirect('Bookmanager:home')
