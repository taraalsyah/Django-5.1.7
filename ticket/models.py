from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Ticket(models.Model):
    id_ticket = models.CharField(primary_key=True, max_length=20, editable=False)
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    category=models.CharField(max_length=50)
    STATUS_CHOICES =(
        (1,'Open'),
        (2,'In-Progress'),
        (3,'Closed')
    )
    status=models.IntegerField(default=1,choices=STATUS_CHOICES)
    assigned_to=models.CharField(max_length=100,blank=True,null=True)
    requested_by=models.CharField(max_length=100)
    attachments=models.FileField(upload_to='attachments/',blank=True,null=True)
    def save(self, *args, **kwargs):
        # generate id_ticket hanya saat create baru
        if not self.id_ticket:
            now = datetime.now()
            # format: MMDDHHMMSS
            self.id_ticket = now.strftime("%m%d%H%M%S")
        super().save(*args, **kwargs)
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

class TicketHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    ticket = models.ForeignKey(
        Ticket,
        to_field='id_ticket',          # ⬅️ RELATE KE id_ticket
        db_column='ticket_id',         # ⬅️ NAMA KOLOM DI TABLE HISTORY
        on_delete=models.CASCADE,
        related_name='histories'
    )
    updated_by = models.CharField(max_length=100)
    comment = models.TextField(null=True, blank=True)
    # snapshot dari ticket.status    
    STATUS_CHOICES =(
        (1,'Open'),
        (2,'In-Progress'),
        (3,'Closed')
    )
    status=models.IntegerField(default=3,choices=STATUS_CHOICES)
    attachment = models.FileField(
        upload_to='ticket_history/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'ticket_history'
        ordering = ['-created_at']
