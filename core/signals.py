# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import SoftwareVersion
# from django.core.exceptions import ValidationError

# @receiver(pre_save, sender=SoftwareVersion)
# def split_version(sender, instance, **kwargs):
#     if instance.version:
#         parts = instance.version.split('.')
#         if len(parts) == 5:
#             try:
#                 instance.tractor_model = parts[0]
#                 instance.engine_comp = parts[1]
#                 instance.first_number = int(parts[2])
#                 instance.second_number = int(parts[3])
#                 instance.third_number = int(parts[4])
#             except:
#                 pass
#     elif instance.tractor_model and instance.engine_comp and instance.first_number and instance.second_number and instance.third_number:
#         instance.version = f"{instance.tractor_model}.{instance.engine_comp}.{instance.first_number}.{instance.second_number}.{instance.third_number}"
#     # else:
#     #     raise ValidationError(f'NULL')
    
