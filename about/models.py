from django.db import models
from .validators import validate
# Create your models here.

class AboutDb(models.Model):
    nama=models.CharField(max_length=100)
    alamat=models.CharField(max_length=10000)
    handphone=models.BigIntegerField(validators=[validate])
    SEX={
        'Man':'Man',
        'Women':'Women'
    }
    sex=models.CharField(max_length=5,choices=SEX,default='Select')
    def __str__(self):
        return "{}. {}".format(self.id , self.nama)

class Ticket(models.Model):
    id_ticket=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    category=models.CharField(max_length=50)
    STATUS_CHOICES =(
        ('Open','Open'),
        ('In Progress','In Progress'),
        ('Pending','Pending'),
        ('Resolved','Resolved'),
        ('Closed','Closed')
    )
    status=models.CharField(max_length=20,default='Open',choices=STATUS_CHOICES)
    assigned_to=models.CharField(max_length=100,blank=True,null=True)
    requested_by=models.CharField(max_length=100)
    attachments=models.FileField(upload_to='attachments/',blank=True,null=True)
    def __str__(self):
        return self.title
    
class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    status = models.CharField(max_length=20, choices=Ticket.STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Comment by {self.author} on Ticket {self.ticket.id}"
    
class Attachment(models.Model):
    id=models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,)
    file = models.FileField(upload_to='ticket_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=100)
    def __str__(self):
        return f"Attachment for Ticket {self.ticket.id}"