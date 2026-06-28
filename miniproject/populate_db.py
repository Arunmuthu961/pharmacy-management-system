import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miniproject.settings')
django.setup()

from pharmacy.models import Medicine

def seed_medicines():
    medicines = [
        {
            'name': 'Paracetamol 500mg',
            'description': 'Effective pain relief for headaches and fever.',
            'price': 5.99,
            'requires_prescription': False
        },
        {
            'name': 'Amoxicillin 250mg',
            'description': 'Antibiotic used to treat bacterial infections.',
            'price': 15.50,
            'requires_prescription': True
        },
        {
            'name': 'Ibuprofen 400mg',
            'description': 'Nonsteroidal anti-inflammatory drug used for reducing fever and treating pain.',
            'price': 7.25,
            'requires_prescription': False
        },
        {
            'name': 'Loratadine 10mg',
            'description': 'Antihistamine that treats symptoms such as itching, runny nose, and sneezing.',
            'price': 12.00,
            'requires_prescription': False
        }
    ]

    for med_data in medicines:
        Medicine.objects.get_or_create(
            name=med_data['name'],
            defaults={
                'description': med_data['description'],
                'price': med_data['price'],
                'requires_prescription': med_data['requires_prescription']
            }
        )
    print("Database seeded with sample medicines successfully.")

if __name__ == '__main__':
    seed_medicines()
