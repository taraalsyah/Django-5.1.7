#!/usr/bin/env python
"""
Script untuk membuat superuser dan sample data
Hanya mengisi database, tidak mengubah backend code
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from ticket.models import Ticket, Category

User = get_user_model()

print("🚀 Creating superuser and sample data...\n")

# 1. Create superuser
print("1️⃣ Creating superuser...")
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("   ✅ Superuser created: admin / admin123")
else:
    admin = User.objects.get(username='admin')
    print("   ⚠️  Superuser already exists")

# 2. Create sample users
print("\n2️⃣ Creating sample users...")
users_data = [
    {'username': 'support1', 'email': 'support1@example.com', 'password': 'support123', 'first_name': 'Support', 'last_name': 'One', 'group': 'Support'},
    {'username': 'support2', 'email': 'support2@example.com', 'password': 'support123', 'first_name': 'Support', 'last_name': 'Two', 'group': 'Support'},
    {'username': 'user1', 'email': 'user1@example.com', 'password': 'user123', 'first_name': 'User', 'last_name': 'One', 'group': 'Operation'},
]

for user_data in users_data:
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        # Add to group
        group = Group.objects.get(name=user_data['group'])
        user.groups.add(group)
        print(f"   ✅ Created user: {user_data['username']} / {user_data['password']}")
    else:
        print(f"   ⚠️  User already exists: {user_data['username']}")

# 3. Create categories
print("\n3️⃣ Creating categories...")
categories_data = [
    {'name': 'Hardware', 'description': 'Hardware related issues'},
    {'name': 'Software', 'description': 'Software and application issues'},
    {'name': 'Network', 'description': 'Network connectivity issues'},
    {'name': 'Security', 'description': 'Security and access issues'},
    {'name': 'Other', 'description': 'Other issues'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f"   ✅ Created category: {cat_data['name']}")
    else:
        print(f"   ⚠️  Category already exists: {cat_data['name']}")

# 4. Create sample tickets
print("\n4️⃣ Creating sample tickets...")
tickets_data = [
    {
        'title': 'Laptop tidak bisa nyala',
        'description': 'Laptop saya tidak bisa menyala sejak pagi. Sudah dicoba charge tapi tetap tidak bisa.',
        'category': 'Hardware',
        'status': 1,  # Open
        'requested_by': 'user1',
        'assigned_to': 'support1'
    },
    {
        'title': 'Tidak bisa login ke email',
        'description': 'Saya lupa password email kantor. Mohon bantuan untuk reset.',
        'category': 'Software',
        'status': 2,  # In-Progress
        'requested_by': 'user1',
        'assigned_to': 'support1'
    },
    {
        'title': 'Internet lambat',
        'description': 'Koneksi internet di ruangan saya sangat lambat. Tidak bisa buka website.',
        'category': 'Network',
        'status': 1,  # Open
        'requested_by': 'user1',
        'assigned_to': 'support2'
    },
    {
        'title': 'Printer error',
        'description': 'Printer di lantai 2 menampilkan error "Paper Jam" padahal tidak ada kertas yang nyangkut.',
        'category': 'Hardware',
        'status': 3,  # Closed
        'requested_by': 'user1',
        'assigned_to': 'support1'
    },
    {
        'title': 'Request install software',
        'description': 'Mohon diinstall Microsoft Office di laptop saya.',
        'category': 'Software',
        'status': 2,  # In-Progress
        'requested_by': 'user1',
        'assigned_to': 'support2'
    },
]

import time
for i, ticket_data in enumerate(tickets_data):
    if not Ticket.objects.filter(title=ticket_data['title']).exists():
        # Add small delay to ensure unique timestamp-based IDs
        if i > 0:
            time.sleep(0.1)
        ticket = Ticket.objects.create(
            title=ticket_data['title'],
            description=ticket_data['description'],
            category=ticket_data['category'],
            status=ticket_data['status'],
            requested_by=ticket_data['requested_by'],
            assigned_to=ticket_data['assigned_to']
        )
        print(f"   ✅ Created ticket: {ticket_data['title']}")
    else:
        print(f"   ⚠️  Ticket already exists: {ticket_data['title']}")

print("\n" + "="*60)
print("✅ Setup completed successfully!")
print("="*60)
print("\n📝 Login Credentials:")
print("   Admin:    admin / admin123")
print("   Support1: support1 / support123")
print("   Support2: support2 / support123")
print("   User1:    user1 / user123")
print("\n🌐 Access URLs:")
print("   Login:     http://localhost:8000/login/")
print("   Dashboard: http://localhost:8000/ticket/dashboard/")
print("   Admin:     http://localhost:8000/admin/")
print("\n🎉 Ready to explore the UI!")
