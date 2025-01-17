from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from User.forms import ContactForm


def UserLogin(request):
    if request.user.is_authenticated:
        return redirect('Bookmanager:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('Bookmanager:home')
                else:
                    if User.objects.filter(username=username).exists():
                        messages.error(request, "رمز عبور اشتباه است.")
                        return render(request, 'login.html')
                    else:
                        messages.error(request, "نام کاربری اشتباه است.")
                        return render(request, 'login.html')

        elif request.method == 'GET':
            return render(request, 'login.html')


def UserSignup(request):
    if request.user.is_authenticated:
        return redirect('Bookmanager:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری قبلاً گرفته شده است.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "این ایمیل قبلاً ثبت شده است.")
            elif password != password2:
                messages.error(request, "رمز عبور و تأییدیه رمز عبور یکسان نیستند.")
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                login(request, user)
                return redirect('Bookmanager:home')

        return render(request, 'signup.html')


def UserLogout(request):
    logout(request)
    return redirect('Bookmanager:home')


def Contact_us(request):
    form = ContactForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ContactForm(data=request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                return redirect('users:contact-us')
        else:
            return redirect('users:login')
    return render(request, 'contact_us.html', {'form': form})
