from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, timedelta

class User(AbstractUser):
    email = models.EmailField(("email address"), blank=True, primary_key=True)
    pass

class Listing(models.Model):

    category_list = [
        ('Antiques', 'Antiques'),
        ('Art', 'Art'),
        ('Baby', 'Baby'),
        ('Books', 'Books'),
        ('Business & Industrial', 'Business & Industrial'),
        ('Cameras & Photo', 'Cameras & Photo'),
        ('Cell Phones & Accessories', 'Cell Phones & Accessories'),
        ('Clothing, Shoes & Accessories', 'Clothing, Shoes & Accessories'),
        ('Coins & Paper Money', 'Coins & Paper Money'),
        ('Collectibles', 'Collectibles'),
        ('Computers/Tablets & Networking', 'Computers/Tablets & Networking'),
        ('Consumer Electronics', 'Consumer Electronics'),
        ('Crafts', 'Crafts'),
        ('Dools & Bears', 'Dools & Bears'),
        ('Entertainment Memorabilia', 'Entertainment Memorabilia'),
        ('Gift Cards & Coupons', 'Gift Cards & Coupons'),
        ('Health & Beauty', 'Health & Beauty'),
        ('Home & Garden', 'Home & Garden'),
        ('Jewelry & Watches', 'Jewelry & Watches'),
        ('Music', 'Music'),
        ('Musical Instruments & Gear', 'Musical Instruments & Gear'),
        ('Pet Supplies', 'Pet Supplies'),
        ('Pottery & Glass', 'Pottery & Glass'),
        ('Real Estate', 'Real Estate'),
        ('Specialty Services', 'Specialty Services'),
        ('Sporting Goods', 'Sporting Goods'),
        ('Sports Mem, Cards & Fan Shop', 'Sports Mem, Cards & Fan Shop'),
        ('Stamps', 'Stamps'),
        ('Tickets & Experiences', 'Tickets & Experiences'),
        ('Toys & Hobbies', 'Toys & Hobbies'),
        ('Travel', 'Travel'),
        ('Video Games & Console', 'Video Games & Console'),
        ('Everything Else', 'Everything Else'),
    ]

    durations = [
        (1, 'One Day'),
        (2, 'Two Days'),
        (3, 'Three Days'),
        (4, 'Four Days'),
        (5, 'Five Days'),
        (6, 'Six Days'),
        (7, 'One Week'),
        (14, 'Two Weeks'),
    ]

    id = models.BigAutoField(primary_key=True)
    title =  models.CharField(max_length=50)
    description = models.TextField()
    duration  = models.IntegerField(choices=durations)
    date_posted = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField()
    closed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    startingbid = models.FloatField(max_length=10, default=0)
    image_url = models.URLField(verbose_name="Image URL")
    availibility = models.BooleanField(default=True)
    category = models.CharField(max_length=30, choices=category_list)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('category',)

    def save(self, *args, **kwargs):
        self.date_end = self.date_posted + timedelta(days=self.duration)
        super().save(*args, **kwargs)

    def ended(self):
        if self.closed or self.end_time < timezone.now():
            return True
        else:
            return False

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
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return f"{self.author} commented: {self.text}"
