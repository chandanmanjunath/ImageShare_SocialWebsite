#importing many to many changed signal
from django.db.models.signals import m2m_changed

from django.dispatch import receiver
from .models import Image



#use decorator to execute users_like_changed function
#sender argiments specifies this receiver will be called only when Image.users_like many to many field is changed
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
        instance.total_likes = instance.users_like.count()
        instance.save()
        
