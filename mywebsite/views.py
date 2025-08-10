from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



@login_required(login_url='index')
@never_cache
def index(request):
    judul="Halo index"
    subjudul="Welcome to my website"
    output=judul+subjudul
    context = {
        'judul':'MyWebsites',
    }
    return render(request,'index.html',context)


def custom_login(request):
    if request.method == "POST":
         
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)

            # Redirect to 'next' if exists, else index
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
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