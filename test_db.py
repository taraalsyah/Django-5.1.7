import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

import django
django.setup()

try:
    from django.db import connection
    connection.ensure_connection()
    print("✅ Database connected successfully!")
except Exception as e:
    print(f"❌ Database connection error:")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    import traceback
    traceback.print_exc()
