from django.core.exceptions import ValidationError



def validate(value):
    from .models import Post
    judulinput = value
    print(judulinput,'va')
    data = Post.objects.all()
    titles = [post.title for post in data]
    if judulinput in titles:
        message = "Maaf data "+judulinput+" sudah tersedia"
        raise ValidationError(message)