from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Bid, Listing

@receiver(post_save, sender=Listing)
def create_bid(sender, instance, created, **kwargs):
    if created:
        Bid.objects.create(bid=instance)