from django.core.exceptions import ValidationError



def validate(value):
    from .models import AboutDb
    judulinput = len(str(value))
    print(len(str(judulinput)),'va')
    #data = AboutDb.objects.all()
    
    if judulinput > 13:
        message = "MSISDN terlalu panjang"
        raise ValidationError(message)