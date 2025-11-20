import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=== Creando usuarios de prueba ===\n")

usuarios = [
    {
        'email': 'usuario@test.com',
        'password': 'Usuario123!',
        'first_name': 'Usuario',
        'last_name': 'Prueba',
        'is_superuser': False
    },
    {
        'email': 'admin@test.com',
        'password': 'Admin123!',
        'first_name': 'Admin',
        'last_name': 'Sistema',
        'is_superuser': True
    },
    {
        'email': 'facundo.cores@gmail.com',
        'password': 'Facundo123!',
        'first_name': 'Facundo',
        'last_name': 'Cores',
        'is_superuser': True
    }
]

for usuario_data in usuarios:
    email = usuario_data['email']
    
    # Eliminar usuario si existe para recrearlo con contraseña válida
    if User.objects.filter(email=email).exists():
        User.objects.filter(email=email).delete()
        print(f"[INFO] Usuario '{email}' existente eliminado")
    
    # Crear usuario
    if usuario_data['is_superuser']:
        user = User.objects.create_superuser(
            username=email,
            email=email,
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
    else:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
    
    role = "Admin" if usuario_data['is_superuser'] else "Usuario"
    print(f"[OK] {role} creado: {email} / {usuario_data['password']}")

print("\n¡Listo! Ahora puedes usar estos usuarios en la app:")
print("   - usuario@test.com / Usuario123!")
print("   - admin@test.com / Admin123!")
print("   - facundo.cores@gmail.com / Facundo123!")

