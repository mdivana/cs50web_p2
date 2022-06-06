from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from PIL import Image


class User(AbstractUser):
    email = models.EmailField(("email address"), blank=True, primary_key=True)
    pass


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    title =  models.CharField(max_length=50)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    startingbid = models.FloatField(max_length=10, default=0, blank=True)
    image = models.ImageField(upload_to='listing_pics')
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlisting")
    availibility = models.BooleanField(default=True)
    category = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *agrs, **kwargs):
        super(Listing, self).save(*agrs, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('listing-detail', kwargs={'pk': self.pk})

class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None, related_name="bid")
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
