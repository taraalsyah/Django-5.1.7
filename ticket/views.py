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
from .forms import TicketForm,TicketHistoryForm, CategoryForm
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
import csv
from django.contrib.auth.decorators import login_required
from ticket.models import Category
from ticket.services.email_services import send_ticket_status_email
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from datetime import datetime
from django.contrib.auth.models import Group




def index(request):
    user = request.user
    email = user.email
    query = request.GET.get('q')
    User = get_user_model()

    # Check if user is Admin or Superuser
    is_admin = user.is_superuser or user.groups.filter(name__iexact='Admin').exists()
    is_engineer = user.groups.filter(name__iexact='Engineer').exists()
    engineers = User.objects.filter(
    groups__name='Engineer',
    is_active=True
    )
    for a in engineers:
        print(a)
    print('engineer',engineers)

    for a in engineers:
        print(a)
    if is_admin:
        tickets = Ticket.objects.all().order_by('status','-created_at')
        role = 'Admin'
    elif is_engineer:
        tickets = Ticket.objects.filter(assigned_to=email).order_by('status','-created_at')
        role = 'Engineer'
    else:
        tickets = Ticket.objects.filter(requested_by=email).order_by('status','-created_at')
        role = 'Operation'

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

    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ticket/index.html', {
        'tickets': tickets,
        'query': query,
        'email': email,
        'page_obj': page_obj,
        'role': role,
        'is_engineer':engineers,
    })

@login_required
def create_ticket(request):
    user = request.user
    username = request.user.username
    user_obj = User.objects.get(username=username)
    email = user_obj.email

    # Base queryset
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        tickets = Ticket.objects.all().order_by('-created_at')
        role = 'Admin'
    elif user.groups.filter(name='Operation').exists():
        tickets = Ticket.objects.filter(requested_by=email).order_by('-created_at')
        role = 'Operation'
    else:
         tickets = Ticket.objects.none() # Or redirect/raise 403
         role = 'User'
    print('Role=',role)

    if request.method == 'POST':
        file = request.FILES.get('attachments')
        user = request.user

        status_code = 1 
        updated_by = request.POST.get('requested_by')



        form = TicketForm(request.POST, request.FILES, user=request.user,is_create=True) # passing user to form
        if form.is_valid():
            ticket=form.save()
            print('DEBUG ticket:', ticket)
            print('DEBUG id_ticket:', ticket.id_ticket)
            TicketHistory.objects.create(ticket=ticket,status=status_code,updated_by=user.username,attachment=file)
            messages.success(request, 'Ticket berhasil dibuat')
            #return JsonResponse({'success': True,'messages': 'Ticket berhasil dibuat','redirect_url': 'ticket/index.html'})
            return redirect('ticket:ticket_index')
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TicketForm(user=request.user,is_create=True) # passing user to form
    return render(request, 'ticket/create_ticket.html', {'form': form,'role':role,'email': email,})


def delete_ticket(request,input):
    postsangka = Ticket.objects.filter(id_ticket=input)
    ticket_id=input
    heading = "Page Delete"
    print(request)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        postsangka.delete()
        return JsonResponse({'success': True,'id_ticket':ticket_id})

    str=heading + input
    context={
        'judul':'Delete',
        'dataurl': str,
        'heading' : heading,
        'Post' : postsangka,
        'lengthchars':10000000,
        }

    return JsonResponse({'success': False}, status=400)


def update(request):
    next_url = (
        request.POST.get('next')
        or request.GET.get('next')
        or '/ticket'
    )

    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()}
    ):
        next_url = '/ticket'
    print("request method:", request.method)
    if request.method == 'POST':
        print('Next URL GET=', request.GET.get('next'))
        print('Next URL POST=', request.POST.get('next'))
        print("Received request to update ticket status")
        data = json.loads(request.body)

        ticket_id = data.get('ticket_id')
        status_code = data.get('status_code')
        comment = request.POST.get('comment')
        attachment = request.FILES.get('attachment')
        updated_by = request.user.username if request.user.is_authenticated else 'system'
        username = request.user.username
        user_obj = User.objects.get(username=username)
        email = user_obj.email
        print(f"Updating ticket {ticket_id} to status {status_code}")

        if status_code not in [1, 2, 3]:
            print('masuk failed')
            return JsonResponse({'success': False, 'error': 'Invalid status code'}, status=400)
        try:
            ticket = Ticket.objects.get(id_ticket=ticket_id)

            # update ticket
            ticket.status = status_code
            ticket.save(update_fields=['status'])

            status_str=''

            if status_code == 1:
                status_str='Open'
            elif status_code == 2:
                status_str='In Progress'
            elif status_code == 3:
                status_str='Closed'
            send_notifikasi_update_status(ticket_id,email,status_str)
            # INSERT history
            if status_code in [1,2]:
                TicketHistory.objects.create(ticket=ticket,status=status_code,comment=comment,updated_by=updated_by,attachment=attachment)

            return JsonResponse({'success': True, 'status': status_str,'ticket_id':ticket_id,'next': next_url},status=200)
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ticket not found','next': next_url},status=400)


def ticket_history(request,ticket_id):
    print("Ticket History for:", ticket_id)
    ticket = get_object_or_404(Ticket, id_ticket=ticket_id)
    status_str=''
    if ticket.status == 1:
        status_str='Open'
    elif ticket.status == 2:
        status_str='In Progress'
    elif ticket.status == 3:
        status_str='Closed'

    print("Ticket found:", ticket.id_ticket)
    if request.method == 'POST':
        form = TicketHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            history = form.save(commit=False)
            history.ticket = ticket
            history.updated_by = request.user
            history.status = ticket.status
            history.save()

            messages.success(request, 'Ticket {} berhasil di Update to {}'.format(ticket_id,status_str))
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
    is_engineer = user.groups.filter(name__iexact='Engineer').exists()

    # Get recent tickets for the table widget
    recent_tickets = Ticket.objects.all().order_by('-created_at')[:5]
    ticket = []
    qs = Ticket.objects.filter(status__in=[1, 2, 3])
    summaryTicket={}
    summaryTicket2={}
    print('cek user=',request.user.groups.filter(name='Operation').exists())
    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        role = 'Admin'
        ticket = qs.values('status').annotate(count=Count('id_ticket'))
        total = sum(row['count'] for row in ticket)
        print('show ticket=',ticket)
        summaryTicket = {
            row['status']: round(row['count'] / total * 100) if total > 0 else 0
            for row in ticket
        }
        print('cek summary=',summaryTicket)
        summaryTicket2 = {
            row['status']: round(row['count'])
            for row in ticket
        }
    elif request.user.groups.filter(name='Operation').exists():
        role = 'Operation'
        print(request.user)
        ticket = qs.filter(requested_by=email).values('status').annotate(count=Count('id_ticket'))
        print('cek ticket=',ticket)
        total = sum(row['count'] for row in ticket)
        summaryTicket = {
            row['status']: round(row['count'] / total * 100) if total > 0 else 0
            for row in ticket
        }
        print('cek summary=',summaryTicket)
        summaryTicket2 = {
            row['status']: round(row['count'])
            for row in ticket
        }
        print('cek summaryTicket2', summaryTicket2)
    elif is_engineer:
        role = 'Engineer'
        ticket = []


    open_count = summaryTicket2.get(1,0)
    progress_count = summaryTicket2.get(2,0)
    closed_count = summaryTicket2.get(3,0)
    print('summary ticket=',summaryTicket,summaryTicket2)

    context = {
        'ticket': summaryTicket,
        'ticket2': summaryTicket2,
        'email': email,
        'role': role,
        'open_count': open_count,
        'progress_count': progress_count,
        'closed_count': closed_count,
        'recent_tickets': recent_tickets,
        'user': user
    }

    return render(request, 'index.html', context)

def get_ticket_status(request):
    username = request.user.username
    user_obj = User.objects.get(username=username)
    email = user_obj.email
    # Fetch the data for auto-refresh (this is the data you'll return as JSON)


    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        total_count = Ticket.objects.count()
        open_count = Ticket.objects.filter(status='1').count()
        in_progress_count = Ticket.objects.filter(status='2').count()
        closed_count = Ticket.objects.filter(status='3').count()
        open_count_percent = round(Ticket.objects.filter(status='1').count() / total_count * 100)
        in_progress_count_percent =round(Ticket.objects.filter(status='2').count() / total_count * 100)
        closed_count_percent =round(Ticket.objects.filter(status='3').count() / total_count * 100)

    elif request.user.groups.filter(name='Operation').exists():
        total_count = Ticket.objects.filter(requested_by=email).count()
        open_count = Ticket.objects.filter(status='1').filter(requested_by=email).count()
        in_progress_count = Ticket.objects.filter(status='2').filter(requested_by=email).count()
        closed_count = Ticket.objects.filter(status='3').filter(requested_by=email).count()

        open_count_percent = round(Ticket.objects.filter(status='1').filter(requested_by=email).count() / total_count * 100)
        in_progress_count_percent =round(Ticket.objects.filter(status='2').filter(requested_by=email).count() / total_count * 100)
        closed_count_percent =round(Ticket.objects.filter(status='3').filter(requested_by=email).count() / total_count * 100)
        print('total_count',total_count)
        
    elif request.user.groups.filter(name='Engineer').exists():
        total_count = Ticket.objects.filter(requested_by=email).count()
        open_count = Ticket.objects.filter(status='1').filter(requested_by=email).count()
        in_progress_count = Ticket.objects.filter(status='2').filter(requested_by=email).count()
        closed_count = Ticket.objects.filter(status='3').filter(requested_by=email).count()

        open_count_percent = round(Ticket.objects.filter(status='1').filter(requested_by=email).count() / total_count * 100)
        in_progress_count_percent =round(Ticket.objects.filter(status='2').filter(requested_by=email).count() / total_count * 100)
        closed_count_percent =round(Ticket.objects.filter(status='3').filter(requested_by=email).count() / total_count * 100)
        print('total_count',total_count)
    
    return JsonResponse({
        'open': open_count,
        'inProgress': in_progress_count,
        'closed': closed_count,
        'openpercent':open_count_percent,
        'inProgresspercent':in_progress_count_percent,
        'closedpercent':closed_count_percent,
        'total_count':total_count,
    })


@login_required
def user_management(request):
    user = request.user
    email = user.email
    groups = Group.objects.all()
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        users = User.objects.all().order_by('-date_joined')
        role = 'Admin'
    else:
        raise Http404("You are not authorized to view this page.")

    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'page_obj': page_obj,
        'role': role,
        'email': email,
        'user': user,
        'groups':groups,
    }

    return render(request, 'ticket/user_management.html', context)


@login_required
def reporting(request):
    user = request.user
    username = request.user.username
    user_obj = User.objects.get(username=username)
    email = user_obj.email

    # Base queryset
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        tickets = Ticket.objects.all().order_by('-created_at')
        role = 'Admin'
    elif user.groups.filter(name='Operation').exists():
        tickets = Ticket.objects.filter(requested_by=email).order_by('-created_at')
        role = 'Operation'
    else:
         tickets = Ticket.objects.none() # Or redirect/raise 403
         role = 'User'

    print('Role=',role)
    # Filters
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    print('Date end=',date_end)
    status = request.GET.get('status')
    category = request.GET.get('category')

    if date_start:
        date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
        tickets = tickets.filter(created_at__date__gte=date_start)
        print('Date Start=',tickets)
    if date_end:
        date_end = datetime.strptime(date_end, "%Y-%m-%d").date()
        tickets = tickets.filter(created_at__date__lte=date_end)
        print('Date end=',tickets)
    if status:
        tickets = tickets.filter(status=status)
        print('Status =',tickets)
    if category:
        tickets = tickets.filter(category=category)
        print('Category=',tickets)

    # Prefetch histories for SLA calculations
    tickets = tickets.prefetch_related('histories')

    # Process SLA data
    for ticket in tickets:
        all_history = list(ticket.histories.all())
        in_progress_history = next((h for h in all_history if h.status == 2), None)
        closed_history = next((h for h in all_history if h.status == 3), None)

        ticket.open_date = ticket.created_at
        ticket.in_progress_date = in_progress_history.created_at if in_progress_history else None
        ticket.closed_date = closed_history.created_at if closed_history else None

        if ticket.open_date and ticket.closed_date:
            ticket.sla_duration = ticket.closed_date - ticket.open_date
        else:
            ticket.sla_duration = None

    # Export to CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ticket_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Title', 'Category', 'Status', 'Assigned To', 'Requested By', 'Open Date', 'In Progress Date', 'Closed Date', 'SLA'])

        for ticket in tickets:
            writer.writerow([
                ticket.id_ticket,
                ticket.title,
                ticket.category,
                ticket.get_status_display(),
                ticket.assigned_to,
                ticket.requested_by,
                ticket.open_date.strftime('%Y-%m-%d %H:%M') if ticket.open_date else '-',
                ticket.in_progress_date.strftime('%Y-%m-%d %H:%M') if ticket.in_progress_date else '-',
                ticket.closed_date.strftime('%Y-%m-%d %H:%M') if ticket.closed_date else '-',
                str(ticket.sla_duration).split('.')[0] if ticket.sla_duration else '-',
            ])
        return response

    # Aggregation for summary cards
    total_count = tickets.count()
    open_count = tickets.filter(status=1).count()
    in_progress_count = tickets.filter(status=2).count()
    print('In Progress =', in_progress_count)
    closed_count = tickets.filter(status=3).count()

    # Get all categories for filter dropdown
    categories = Category.objects.all()

    # Pagination
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Re-calculate history for paginated results if not already pre-fetched correctly by Paginator
    # Actually Paginator should keep the prefetched data if passed correctly.

    context = {
        'tickets': page_obj,
        'page_obj': page_obj,
        'total_count': total_count,
        'open_count': open_count,
        'in_progress_count': in_progress_count,
        'closed_count': closed_count,
        'categories': categories,
        'role': role,
        'email': email,
        # Preserve filter values in context
        'date_start': date_start,
        'date_end': date_end,
        'status_val': status,
        'category_filter': category, 
    }

    return render(request, 'ticket/reporting.html', context)


@login_required
@csrf_exempt
def update_user_role(request):
    """
    Update a user's role by clearing their groups and adding the selected one.
    Only accessible by superusers or members of the 'Admin' group.
    """
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Body Update Role=',data)
            user_id = data.get('user_id')
            new_role = data.get('role')
            print('New Role=',new_role)
            if not user_id:
                return JsonResponse({'success': False, 'error': 'User ID is required'}, status=400)

            user_to_update = get_object_or_404(User, id=user_id)

            # Prevent self-demotion if the current user is an Admin
            if user_to_update == request.user and not request.user.is_superuser:
                 return JsonResponse({'success': False, 'error': 'You cannot update your own role.'}, status=400)

            # Clear existing groups
            user_to_update.groups.clear()

            # Add new group if applicable
            if new_role and new_role != 'None':
                
                group, created = Group.objects.get_or_create(name=new_role)
                user_to_update.groups.add(group)

            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@login_required
@csrf_exempt
def delete_user(request):
    """
    Delete a user.
    Only accessible by superusers or members of the 'Admin' group.
    """
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({'success': False, 'error': 'User ID is required'}, status=400)

            user_to_delete = get_object_or_404(User, id=user_id)
            
            # Prevent self-deletion
            if user_to_delete == request.user:
                 return JsonResponse({'success': False, 'error': 'You cannot delete your own account.'}, status=400)

            user_to_delete.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@login_required
@csrf_exempt
def edit_user(request):
    """
    Handle fetching user data and updating user profile details.
    Only accessible by superusers or members of the 'Admin' group.
    """
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'error': 'User ID is required'}, status=400)
        
        user_to_edit = get_object_or_404(User, id=user_id)
        return JsonResponse({
            'success': True,
            'user': {
                'id': user_to_edit.id,
                'username': user_to_edit.username,
                'email': user_to_edit.email,
                'first_name': user_to_edit.first_name,
                'last_name': user_to_edit.last_name,
            }
        })

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            username = data.get('username')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')

            if not user_id:
                return JsonResponse({'success': False, 'error': 'User ID is required'}, status=400)

            user_to_update = get_object_or_404(User, id=user_id)
            
            # Simple validation: prevent duplicate username if changed
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)

            user_to_update.username = username
            user_to_update.first_name = first_name
            user_to_update.last_name = last_name
            user_to_update.save()

            return JsonResponse({
                'success': True,
                'full_name': user_to_update.get_full_name() or user_to_update.username
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)



@login_required
@csrf_exempt
def toggle_user_status(request):
    """
    Toggle a user's is_active status.
    Only accessible by superusers or members of the 'Admin' group.
    """
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({'success': False, 'error': 'User ID is required'}, status=400)

            user_to_toggle = get_object_or_404(User, id=user_id)
            
            # Prevent self-deactivation
            if user_to_toggle == request.user:
                 return JsonResponse({'success': False, 'error': 'You cannot deactivate your own account.'}, status=400)

            user_to_toggle.is_active = not user_to_toggle.is_active
            user_to_toggle.save()

            return JsonResponse({
                'success': True,
                'is_active': user_to_toggle.is_active
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def send_notifikasi_update_status(ticket,email,status):
    
    subject = f"Status Ticket {ticket}"
    message = f"Your Ticket Has Been Updated to {status}\n\n regards,\nTicket System"
    
    send_mail(
        subject,    
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

@login_required
def category_management(request):
    """
    List categories and handle adding new categories.
    Only accessible by superusers or members of the 'Admin' group.
    """
    if not (request.user.is_superuser or request.user.groups.filter(name__iexact='Admin').exists()):
        raise Http404("You are not authorized to view this page.")

    user = request.user
    email = user.email
    role = 'Admin'

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('ticket:category_management')
    else:
        form = CategoryForm()

    categories = Category.objects.all().order_by('name')
    
    # Pagination
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': page_obj,
        'page_obj': page_obj,
        'form': form,
        'role': role,
        'email': email,
    }
    return render(request, 'ticket/category_management.html', context)

@login_required
@csrf_exempt
def delete_category(request, category_id):
    user = request.user
    
    
    # Check if user is Admin or Superuser
    is_admin = user.is_superuser or user.groups.filter(name__iexact='Admin').exists()
    is_engineer = user.groups.filter(name__iexact='Engineer').exists()
    
    if is_admin:
        role = 'Admin'
    elif is_engineer:
        role = 'Engineer'
    else:
        role = 'Operation'
        
    """
    Delete a category.
    Only accessible by superusers or members of the 'Admin' group.
    """
    if not (request.user.is_superuser or request.user.groups.filter(name__iexact='Admin').exists()):
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return JsonResponse({'success': True,'role':role})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e),'role':role}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method', 'role':role}, status=405)