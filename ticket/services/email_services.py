# services/email_service.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_ticket_status_email(ticket):
    html = render_to_string('ticket/ticket_status_changed.html', {
        'ticket': ticket
    })

    email = EmailMultiAlternatives(
        subject=f'Status Ticket #{ticket.id} Berubah',
        body=f'Status ticket kamu sekarang: {ticket.status}',
        from_email=None,
        to=[ticket.user.email]
    )
    email.attach_alternative(html, 'text/html')
    email.send()
