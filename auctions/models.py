from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    email = models.EmailField(("email address"), blank=True, primary_key=True)
    pass


class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    title =  models.CharField(max_length=50)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, default=None, related_name="listings")
    image = models.ImageField()
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlistings")
    category = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('listing-detail', kwargs={'pk': id})

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
