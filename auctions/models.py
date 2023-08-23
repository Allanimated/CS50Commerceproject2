from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name=models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    class Meta:

        verbose_name_plural='categories'

    def __str__(self):
        return self.name
    
class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    price = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner =models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    active = models.BooleanField()
   
    def __str__(self):
        return self.title
        
    
class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listingcomments")
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.comment}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userwatchlist")
    listed = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.user}: {self.listed}"

class Bids(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listingbids")
    bid = models.PositiveSmallIntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userbids")
    class Meta:

        verbose_name_plural='Bids'

    def __str__(self):
        return f"{self.bidder} has bidded ${self.bid} on {self.listing}"

