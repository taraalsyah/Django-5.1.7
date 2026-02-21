from django.http import HttpResponse,JsonResponse
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
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse,reverse_lazy
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from urllib.parse import urlencode
import os
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import EmailVerificationCode
from django.shortcuts import render

User = get_user_model()


from django.http import HttpResponse

def landing_page(request):
    return render(request, 'landing_page.html')


def debug_url(request):
    return HttpResponse(request.build_absolute_uri())



def error_400(request, exception):
    return render(request, "400.html", status=400)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the user instance but don't commit it yet
            user = form.save(commit=False)
            user.is_active = False  # User can't log in until they verify their email
            user.save()  # Save the user to the database
            
            # Add the user to the Operator group
            user = User.objects.get(username=user.username)
            Operation_group = Group.objects.get(name='Operation')
            user.groups.add(Operation_group)

            # Kirim email verifikasi
            send_verification_email(request, user)
            #send_verification_code(user.email)
            print("user registered:",user.username,user.email)
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            # login(request, user)  # auto login after register
            return redirect("/login/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_url = request.build_absolute_uri(
        reverse("verify_email", kwargs={"uidb64": uid, "token": token})
    )
    print('Verify URL=',verify_url)
    subject = "Verifikasi Akun Anda"
    message = f"Halo {user.username}, klik link berikut untuk verifikasi akun:\n\n{verify_url}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_verification_code(email):
    code = str(random.randint(100000, 999999))
    
    # Hapus kode lama dari email yg sama
    EmailVerificationCode.objects.filter(email=email).delete()

    # Simpan kode baru ke DB
    EmailVerificationCode.objects.create(email=email, code=code)
    
    subject = "Your Verification Code"
    message = f"Your verification code is {code}. Code valid for 5 minutes."
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    
    return code

def resend_verification(request):
    print("masuk resend verification",request.user)
    user = request.user

    if user.email_verified:
        # Kalau sudah verified, redirect ke halaman success
        return redirect("verify-success")

    # Kirim ulang email verifikasi
    send_verification_email(user, request)

    # Bisa redirect ke halaman "email dikirim" atau tampil pesan
    return JsonResponse({"success": True, "message": "Email verifikasi telah dikirim ulang."})


def verify_account(request, uid, token):
    print('masuk verify account',uid,token,request.method,request.headers.get('X-Requested-With'))
    print("HEADERS:", request.headers)
    #print("META:", request.META)
    # Jika ini request pertama (GET biasa) → tampilkan halaman loading
    if request.method == "GET" and request.headers.get('x-requested-with') != 'XMLHttpRequest':
        
        print('ini uid=',uid)
        return render(request, 'verify.html')

    # Jika ini request AJAX (POST via fetch)
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print('ini uid post=',uid)
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
            # Cek apakah token valid
            if user.verification_token == token:
                user.is_active = True
                user.verification_token = ""
                user.verified_at = now()
                user.save()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "message": "Invalid token"})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found"})

    return JsonResponse({"success": False, "message": "Invalid request"})



def verify_success(request):
    """
    Show a success message after successful email verification.
    """
    return render(request, 'verify_success.html')

def verify_failed(request):
    """
    Show an error message if verification fails.
    """
    return render(request, 'verify_failed.html')

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email successfully verified! You can now log in.")
        return redirect("login")
        
    else:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("register")
    

def send_test_email():
    subject = "Email Test Django"
    message = "Halo! Ini email test dari Django dengan SSL aman."
    sender = settings.EMAIL_HOST_USER
    recipient = ["taraalsyah45@gmail.com"]

    send_mail(subject, message, sender, recipient, fail_silently=False)


@never_cache
def index(request):
    username = request.user.username
    user_obj = User.objects.get(username=username)
    first_name = user_obj.first_name
    last_name = user_obj.last_name
    email = user_obj.email
    phone_number = user_obj.phone_number if hasattr(user_obj, 'phone_number') else 'N/A'
    print('ini first name',first_name)
    print('ini last name',last_name)
    print('ini email',email)
    print('ini phone number',phone_number)
    print('ini user obj',user_obj)
    print('ini index',username)
    judul="Halo index"
    subjudul=f"Welcome to my website, {username}"
    print(subjudul)
    print("User di index:", request.user, request.user.is_authenticated)
    context = {
        'judul':'MyWebsites',
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone_number': phone_number,
    }
    return render(request,'index.html',context)


def custom_login(request):
    # Kalo session user = login > langsung ke dashboard
    
    print(request.META.get("REMOTE_ADDR"))
    print(request.META.get("HTTP_X_FORWARDED_FOR"))
    
    if request.user.is_authenticated:
        return redirect('ticket:dashboard')

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
            messages.success(request, f"Successfully Login as {username}")
            return redirect('/ticket/dashboard/')  # redirect ke halaman tujuan
        else:
            messages.error(request, "Invalid username or password.")
        
    return render(request, "login.html")


def logout_view(request):
    next_url = request.GET.get('next', '/')
    
    print('Next URL=',next_url)
    logout(request)  # Clears the session  
    login_url = reverse('login')
    
    response = redirect(f'{login_url}?next={next_url}')
    # Prevent browser from caching authenticated pages
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return redirect(next_url)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'   # halaman template
    success_url = reverse_lazy('index')          # redirect ke profile setelah sukses

    def form_valid(self, form):
        messages.success(self.request, "Password berhasil diperbarui")
        return super().form_valid(form)
    
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    email=user.email
    first_name = user.first_name
    last_name = user.last_name
    phone_number= user.phone_number
    first_group = request.user.groups.first()
    role = first_group.name if first_group else 'User'
    print('Role=',role)
    context = {
        'user': user,
        'judul':'Profile',
        'email': email,
        'username': user.username,
        'role':role,
        'first_name':first_name,
        'last_name':last_name,
        'phone_number':phone_number,
    }
    return render(request, 'profile.html', context)

#def unlink_google(request):
#    try:
#        account = SocialAccount.objects.get(user=request.user, provider="google")
#        account.delete()
#        messages.success(request, "Google account successfully unlinked.")
#    except SocialAccount.DoesNotExist:
#        messages.error(request, "No Google account linked.")
#    return redirect("profile")  # change to your profile page name

@login_required
def unlink_social(request, pk):
    account = get_object_or_404(SocialAccount, pk=pk, user=request.user)
    account.delete()
    messages.success(request, "Akun berhasil dihapus.")
    return redirect("socialaccount_connections")


def security_view(request):
    user = request.user
    username = request.user.username
    user_obj = User.objects.get(username=username)
    email = user_obj.email

    # Base queryset
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        role = 'Admin'
    elif user.groups.filter(name='Operation').exists():
        role = 'Operation'
    else:
         role = 'Engineer'
         
    print('Role=',role)
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    
    context = {
        'user': user,
        'judul':'Security',
        'email': user.email,
        'role':role
    }
    return render(request, 'security.html', context)





def check_ip(request):
    return JsonResponse({
        "REMOTE_ADDR": request.META.get("REMOTE_ADDR"),
        "X_FORWARDED_FOR": request.META.get("HTTP_X_FORWARDED_FOR"),
    })