from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from mywebsite.adapters import User
import ticket
from ticket.models import Ticket,TicketHistory
#from .models import Ticket,TicketHistory
from django.db.models import Q,Count
from django.http import HttpResponse,JsonResponse, Http404
from .forms import TicketForm,TicketHistoryForm
from django.contrib import messages


def index(request):
    user = request.user
    username = request.user.username
    user_obj = User.objects.get(username=username)
    email = user_obj.email
    query = request.GET.get('q')
    
    if user.is_superuser:
        tickets = Ticket.objects.all().order_by('-created_at')  # ambil semua tiket
        role = 'Admin'
    else:
        # Operation user can only see tickets assigned to him/her
        if user.groups.filter(name='Operation').exists():
            tickets = Ticket.objects.filter(requested_by=email).order_by('-created_at')
            role = 'Operation'
        else:
            raise Http404("You are not authorized to view this page.")
    if query:
        tickets = tickets.filter(
            Q(id_ticket__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(status__icontains=query) |
            Q(assigned_to__icontains=query) |
            Q(requested_by__icontains=query) |
            Q(created_at__icontains=query)
        ).order_by('-created_at')
    paginator = Paginator(tickets, 10)  # 10 data per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print('Paginator Object', page_obj)
    print(user.groups.filter(name='operation'))
    
    
    return render(request, 'ticket/index.html', {'tickets': tickets,'query': query, 'email': email,'page_obj': page_obj,'role':role})

def create_ticket(request):
    if request.method == 'POST':
        file = request.FILES.get('attachments')
        
        print("File uploaded:", file)
        form = TicketForm(request.POST, request.FILES, user=request.user,is_create=True) # passing user to form
        if form.is_valid():
            form.save()
            
            #return JsonResponse({'success': True,'messages': 'Ticket berhasil dibuat','redirect_url': 'ticket/index.html'})
            return redirect('ticket:ticket_index')
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TicketForm(user=request.user,is_create=True) # passing user to form
    return render(request, 'ticket/create_ticket.html', {'form': form})


def delete_ticket(request,input):
    postsangka = Ticket.objects.filter(id_ticket=input)
    heading = "Page Delete"
    print(request)
    if request.method == 'POST':
        postsangka.delete()
        return redirect('ticket:ticket_index')

    str=heading + input
    context={
        'judul':'Delete',
        'dataurl': str,
        'heading' : heading,
        'Post' : postsangka,
        'lengthchars':10000000,
        }

    return render(request,'ticket/ticket.html',context)


def update(request):
    print("request method:", request.method)
    if request.method == 'POST':
        print("Received request to update ticket status")
        data = json.loads(request.body)

        ticket_id = data.get('ticket_id')
        status_code = data.get('status_code')
        
        print(f"Updating ticket {ticket_id} to status {status_code}")

        if status_code not in [1, 2, 3]:
            print('masuk failed')
            return JsonResponse({'success': False, 'error': 'Invalid status code'}, status=400)
        try:
            ticket = Ticket.objects.get(id_ticket=ticket_id)
            ticket.status = status_code
            ticket.save(update_fields=['status'])
            print('Masuk Success',ticket.status)
            return JsonResponse({'success': True, 'status': ticket.status},status=200)
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ticket not found'},status=400)
        
        
def ticket_history(request,ticket_id):
    print("Ticket History for:", ticket_id)
    ticket = get_object_or_404(Ticket, id_ticket=ticket_id)
    print("Ticket found:", ticket.id_ticket)
    if request.method == 'POST':
        form = TicketHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            history = form.save(commit=False)
            history.ticket = ticket
            history.updated_by = request.user
            history.status = ticket.status
            history.save()
            return redirect('ticket:ticket_index')
    else:
        form = TicketHistoryForm(initial={'ticket': ticket, 'updated_by': request.user})
        
    return render(request, 'ticket/ticket_history.html', {'form': form, 'ticket': ticket})

def showHistory(request,ticketId):
    tickets = TicketHistory.objects.filter(ticket_id=ticketId)
    print('Ticket History:',tickets)
    return render(request, 'ticket/showHistory.html', {'tickets': tickets})

def dashboard(request):
    username = request.user.username
    user_obj = User.objects.get(username=username)
    email = user_obj.email
    user = request.user
    
    ticket = Ticket.objects.values('status').filter(status__in=[1,2,3]).annotate(count=Count('id_ticket'))
    print('Ticket Dashboard',ticket)
    total = sum(row['count'] for row in ticket)
    print('Total Ticket:',total)
    
    total_count = Ticket.objects.count()
    print('Total Count:',total_count)
    open_count = Ticket.objects.filter(status='1').count()
    in_progress_count = Ticket.objects.filter(status='2').count()
    closed_count = Ticket.objects.filter(status='3').count()
    print('Total status:',open_count,in_progress_count,closed_count)
    summaryTicket = {
        row['status']: round(row['count'] / total * 100)
        for row in ticket
    }
    summaryTicket2 = {
        row['status']: round(row['count'])
        for row in ticket
    }
    if user.is_superuser:
        role = 'Admin'
    else:
        if user.groups.filter(name='Operation').exists():
            role = 'Operation'
    return render(request, 'ticket/dashboard.html', {'ticket': summaryTicket,'ticket2' : summaryTicket2, 'email': email,'role':role,'open': open_count,'inProgress': in_progress_count,'closed': closed_count})
    
def get_ticket_status(request):
    # Fetch the data for auto-refresh (this is the data you'll return as JSON)
    total_count = Ticket.objects.count()
    open_count = Ticket.objects.filter(status='1').count()
    in_progress_count = Ticket.objects.filter(status='2').count()
    closed_count = Ticket.objects.filter(status='3').count()

    open_count_percent = round(Ticket.objects.filter(status='1').count() / total_count * 100)
    in_progress_count_percent =round(Ticket.objects.filter(status='2').count() / total_count * 100)
    closed_count_percent =round(Ticket.objects.filter(status='3').count() / total_count * 100)
    # Return updated data as JSON
    return JsonResponse({
        'open': open_count,
        'inProgress': in_progress_count,
        'closed': closed_count,
        'openpercent':open_count_percent,
        'inProgresspercent':in_progress_count_percent,
        'closedpercent':closed_count_percent
    })