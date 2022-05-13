from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    email = models.EmailField(("email address"), blank=True, primary_key=True)
    pass

class Bids(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bid of {self.bid} by {self.user}"

class Listings(models.Model):
    title =  models.CharField(max_length=50)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.ForeignKey(Bids, on_delete=models.CASCADE, default=None)
    image = models.ImageField()
    watchlist = models.ManyToManyField(User, blank=True)
    category = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return f"{self.title}: {self.bid}"
        
    def get_url(self):
        return reverse('listing-detail', kwargs={'pk': self.pk})

class Comments(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
