from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse,reverse_lazy
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from urllib.parse import urlencode
import os
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False   # ⛔ User belum bisa login
            user.save()
            #user = form.save()
            # Kirim email verifikasi
            send_verification_email(request, user)
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            # login(request, user)  # auto login after register
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_url = request.build_absolute_uri(
        reverse("verify_email", kwargs={"uidb64": uid, "token": token})
    )

    subject = "Verifikasi Akun Anda"
    message = f"Halo {user.username}, klik link berikut untuk verifikasi akun:\n\n{verify_url}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return HttpResponse("Link verifikasi tidak valid / kadaluarsa.")

def send_test_email():
    subject = "Email Test Django"
    message = "Halo! Ini email test dari Django dengan SSL aman."
    sender = settings.EMAIL_HOST_USER
    recipient = ["taraalsyah45@gmail.com"]

    send_mail(subject, message, sender, recipient, fail_silently=False)


@never_cache
def index(request):
    username = request.user.username
    print('ini index',username)
    judul="Halo index"
    subjudul=f"Welcome to my website, {username}"
    print(subjudul)
    print("User di index:", request.user, request.user.is_authenticated)
    context = {
        'judul':'MyWebsites',
        'username': username,
    }
    return render(request,'index.html',context)


def custom_login(request):
    if request.method == "POST":
         
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next") or reverse("index")
        user = authenticate(request, username=username, password=password)

        print(username)
        print(password)
        print(user)
        print("POST data:", request.POST)

        if user is not None:
            login(request, user)
            return redirect(next_url)  # redirect ke halaman tujuan
        else:
            messages.error(request, "Invalid username or password.")
        
    return render(request, "login.html")


def logout_view(request):
    logout(request)  # Clears the session
    response = redirect('login')
    # Prevent browser from caching authenticated pages
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'   # halaman template
    success_url = reverse_lazy('index')          # redirect ke profile setelah sukses

    def form_valid(self, form):
        messages.success(self.request, "Password berhasil diperbarui")
        return super().form_valid(form)
    
