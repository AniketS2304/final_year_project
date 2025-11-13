import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriwise_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
username = 'admin'
email = 'admin@agriwise.com'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f"✅ Admin user '{username}' already exists!")
    user = User.objects.get(username=username)
    # Reset password
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"🔄 Password reset for '{username}'")
else:
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Created superuser '{username}'")

print("\n" + "="*60)
print("Django Admin Credentials:")
print("="*60)
print(f"URL:      http://127.0.0.1:8000/admin/")
print(f"Username: {username}")
print(f"Password: {password}")
print("="*60)
