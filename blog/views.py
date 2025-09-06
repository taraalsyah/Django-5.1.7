from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Post,City,Country
from django.urls import re_path,path
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from .forms import LocationForm, PostForm
from django.contrib import messages
import csv
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-id') # urutkan dari terbaru
    # Ambil query search dan filter
    search_query = request.GET.get('search', '')
    
    category_filter = request.GET.get('category', '')

    # Filter berdasarkan search
    if search_query:
        posts = posts.filter(title__icontains=search_query)

    # Filter berdasarkan kategori
    if category_filter:
        posts = posts.filter(category__iexact=category_filter)

    # Pagination (5 data per halaman)
    paginator = Paginator(posts, 5) # 5 item per halaman
    page_number = request.GET.get('page')
    print(page_number)
    page_obj = paginator.get_page(page_number)

    context={
        'judul':'BLOG',
        'nav':[
            ['/','Home'],
            ['blog/','Article'],
            ['about/','Post']
        ],
        'banner':'blog/img/data.pdf.jpeg',
        'appcss':'blog/css/styles.css',
        'Post' : posts,
        'lengthchars':100,
        'heading':'Halaman Utama Index Blog',
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,

    }
    return render(request,'blog/blog.html',context)

def delete(request,input):
    postsangka = Post.objects.filter(id=input)
    heading = "Page Delete"
    print(request)
    if request.method == 'POST':
        postsangka.delete()
        return HttpResponseRedirect('/blog/')
    
    str=heading + input
    context={
        'judul':'Delete',
        'dataurl': str,
        'heading' : heading,
        'Post' : postsangka,
        'lengthchars':10000000,
        }
        
    return render(request,'blog/blog.html',context)


def slugpost(request,sluginput):
    postsslug = Post.objects.filter(slug=sluginput)
    heading = "Slug Post"
    str=heading + sluginput
    context={
        'judul':'Slug',
        'dataurl': str,
        'heading' : heading,
        'Post' : postsslug,
        'lengthchars':10000000,
    }

    return render(request,'blog/blog.html',context)

def create(request):
    country_id = request.GET.get('country_id')  # ✅ Always defined
    # Handle AJAX for dynamic city loading
    print('ini x-request=',request.headers.get('x-requested-with'))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        country_id = request.GET.get('country_id')
    if country_id:
        cities = City.objects.filter(country_id=country_id).order_by('name')
        return JsonResponse(list(cities.values('id', 'name')), safe=False)

    post_form = PostForm(request.POST or None)
    location_form = LocationForm(request.POST or None)
    print(post_form,'create')

    if request.method == 'POST':
        if post_form.is_valid() and location_form.is_valid():
            post = post_form.save(commit=False)
            post.country = location_form.cleaned_data['country']
            post.city = location_form.cleaned_data['city']
            post.save()
            print(post.save,'save')
            messages.success(request, "Post created successfully!")
            #return HttpResponseRedirect("/blog/")
            return redirect('blog:index')
        else:
            print("Post form errors:", post_form.errors)
            print("Location form errors:", location_form.errors)

    context={
        'judul':'Create',
        'post_form':post_form,
        'location_form':location_form,
    }
    return render(request,'blog/create.html',context)

def update(request,update_id):
    product = get_object_or_404(Post, id=update_id)
    print(product)
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        category = request.POST.get("category")
        print(title)
        # Update fields
        product.title = title
        product.body = body
        product.category = category
        product.save()  # Save changes

        messages.success(request, "Product updated successfully!")
        return redirect('/blog/')  # Redirect after upda
    context={
        'judul':'Update',
        'post_form':product,
        'heading':'Halaman Update'
    }
    return render(request,'blog/update.html',context)


def download_posts_csv(request):
    category = request.GET.get("category")
    search = request.GET.get("search")
    print('ini category',category)
    print('ini search',search)
    
    queryset = Post.objects.all()
    
    if search:
        queryset = queryset.filter(title__icontains=search)

    if category:
        queryset = queryset.filter(category__iexact=category)

    # Response dengan header CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'

    writer = csv.writer(response)
    # Header kolom
    writer.writerow(['title', 'body', 'category'])

    # Ambil data dari MySQL
    for post in queryset:
        writer.writerow([post.title, post.body, post.category])
        

    return response