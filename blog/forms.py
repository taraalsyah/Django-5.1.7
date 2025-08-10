from django import forms
from django.core.exceptions import ValidationError
from .models import Post



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[
            'title',
            'body',
            'category',
        ]



#class PostForm(forms.Form):
#    title = forms.CharField(max_length=20)
#    body  = forms.CharField(
#        widget=forms.Textarea
#    )
#    category = forms.CharField()

#    def clean(self):
#        data = Post.objects.all()
#        titles = [post.title for post in data]
#        judulinput = self.cleaned_data.get('title')
#        
#        #cek double data input
#        if judulinput in titles:
#            raise ValidationError("tara adalah admin")
#        return judulinput    