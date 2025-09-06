from django import forms
from django.core.exceptions import ValidationError
from .models import Post,Country,City,Tara



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[
            'title',
            'body',
            'category',
        ]


class LocationForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        label="Country"
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        label="City"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If country already selected (e.g., after form submit)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass


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