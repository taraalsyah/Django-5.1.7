from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView,TemplateResponseMixin
from django.views.generic.edit import CreateView,UpdateView
from django.http import HttpResponse,HttpResponseRedirect
from .forms import AboutForm
from .models import AboutDb
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
# Create your views here.

def about_page(request):
    return render(request, "about/index.html")

class IndexClassView(View):
    template_name = 'about/about.html'
    context = {}
    def get(self,request):
        print(request,'ini dari get index')
        print(AboutForm)
        context = {
        'judul':'About',
        'heading':'Class Based View GET',
        'form':AboutForm,
        'appcssabout':'static/about/css/styles.css',
        }
        return render(request,self.template_name,context)
    
    def post(self,request):
        post_form=AboutForm(request.POST)                                                         
        post_form.save()
        context = {
        'judul':'About',
        'heading':'Class Based View POST',
        'appcssabout':'about/css/styles.css',
        }
        
        return redirect("about:index")

class Template(TemplateView):
    template_name='about/templateview.html'
    extra={'nama':'tara'}
    def get_context_data(self,*args,**kwargs):
        kwargs.update(self.extra)
        print(super().get_context_data(*args,**kwargs))
        p=kwargs['parameter']
        #print(p)
        context={
            'heading':'Template View 1',
            'params':p
        }
        return context
    
class Createview(CreateView):
    template_name = 'about/createview.html'
    model=AboutDb
    success_url = reverse_lazy('about:index')
    print('ini create view')
    fields=[
        'nama',
        'alamat',
        'handphone',
        'sex',
    ]
    extra_context={
        'judul':'Create View'
    }
    def get_context_data(self, **kwargs):
        kwargs.update(self.extra_context)
        return super().get_context_data(**kwargs)
    
class Updateview(UpdateView):
    template_name='about/createview.html'
    model=AboutDb
    success_url = reverse_lazy('about:index')
    fields=[
        'alamat',
        'handphone',
        'sex',
    ]
    extra_context={
        'judul':'Update View'
    }
    def get_context_data(self, **kwargs):
        kwargs.update(self.extra_context)
        return super().get_context_data(**kwargs)

class Listview(ListView):
    model=AboutDb
    print('ini list view')
    template_name='about/listview.html'
    ordering=['sex']
    paginate_by=2
    paginate_orphans = 0
    fields=[
        'alamat',
        'handphone',
        'sex',
    ]
    extra_context={
        'judul':'List View',
        'field':fields
    }
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.extra_context)
        return super().get_context_data(**kwargs)
    
class Ubsi(View):
    template_name = 'about/ubsi.html'
    context = {}
    def get(self,request):
        print(request,'ini dari get index')
        print(AboutForm)
        context = {
        'judul':'About',
        'heading':'Class Based View GET',
        'form':AboutForm,
        'appcssabout':'static/about/css/styles.css',
        }
        return render(request,self.template_name,context)