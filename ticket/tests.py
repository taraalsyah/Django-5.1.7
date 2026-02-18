from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from ticket.models import Ticket, TicketHistory
from datetime import timedelta
from django.utils import timezone

class ReportingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='admin', password='password123', email='admin@example.com')
        self.client.login(username='admin', password='password123')
        
        # Create a ticket
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            category='Bug',
            requested_by='user@example.com'
        )
        
        # Add history
        # Status 1 (Open) is created automatically in view, but here we add manually if needed
        # Actually TicketHistory is created in views.create_ticket
        TicketHistory.objects.create(ticket=self.ticket, status=1, updated_by='admin')
        
        # Move to In Progress (Status 2)
        TicketHistory.objects.create(ticket=self.ticket, status=2, updated_by='admin')
        
        # Move to Closed (Status 3)
        TicketHistory.objects.create(ticket=self.ticket, status=3, updated_by='admin')

    def test_reporting_view_status_code(self):
        response = self.client.get(reverse('ticket:reporting'))
        self.assertEqual(response.status_code, 200)

    def test_reporting_view_context(self):
        response = self.client.get(reverse('ticket:reporting'))
        tickets = response.context['tickets']
        found_ticket = None
        for t in tickets:
            if t.id_ticket == self.ticket.id_ticket:
                found_ticket = t
                break
        
        self.assertIsNotNone(found_ticket)
        self.assertIsNotNone(found_ticket.open_date)
        self.assertIsNotNone(found_ticket.in_progress_date)
        self.assertIsNotNone(found_ticket.closed_date)
        self.assertIsNotNone(found_ticket.sla_duration)
        
    def test_reporting_csv_export(self):
        response = self.client.get(reverse('ticket:reporting') + '?export=csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Open Date', content)
        self.assertIn('In Progress Date', content)
        self.assertIn('Closed Date', content)
        self.assertIn('SLA', content)
