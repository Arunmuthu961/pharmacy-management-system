import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miniproject.settings')
django.setup()

from pharmacy.models import Medicine

image_map = {
    'Paracetamol 500mg': 'medicines/Paracetamol.jpeg',
    'Amoxicillin 250mg': 'medicines/Amoxicillin.jpeg',
    'Ibuprofen 400mg': 'medicines/Combiflam.jpeg', 
    'Loratadine 10mg': 'medicines/Cetrizine.jpeg'
}

for name, img_path in image_map.items():
    med = Medicine.objects.filter(name=name).first()
    if med:
        med.image = img_path
        med.save()
print("Images updated")
