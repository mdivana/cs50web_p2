from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse
from PIL import Image


class User(AbstractUser):
    email = models.EmailField(("email address"), blank=True, primary_key=True)
    pass


class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    title =  models.CharField(max_length=50)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, default=None, related_name="listing")
    image = models.ImageField(upload_to='listing_pics')
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlisting")
    category = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *agrs, **kwargs):
        super(Listing, self).save(*agrs, **kwargs)

        img = Image.open(self.image.path)
        img.save(self.image.path)

    def get_url(self):
        return reverse('listing-detail', kwargs={'pk': id})

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
