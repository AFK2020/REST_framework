from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Timeline

@receiver(post_save, sender=Project)
def create_timeline_on_project_save(sender, instance, created, **kwargs):
    if created:
        Timeline.objects.create(project=instance)