from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, AuctionListing,Comment, Watchlist, Bids, Category
from .forms import AuctionListingForm
from django.contrib import messages



def index(request):
    listings = AuctionListing.objects.all()
    context = {'listings': listings}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def new_listing(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST,request.FILES, current_user=request.user)
        
        if form.is_valid():

            form.save()
            
            return HttpResponseRedirect(reverse("auctions:index"))
    else:
        form = AuctionListingForm(current_user=request.user)

    context= {'form': form}
    return render(request, "auctions/new_listing.html", context)


@login_required
def place_bid(request, listing_id):
    if request.method == 'POST' and 'bid' in request.POST:
        new_bid = request.POST['bid']
        listing = get_object_or_404(AuctionListing, id=listing_id)
        
        if not new_bid:
            message = 'Please provide a valid bid.'
        else:
            try:
                new_bid = int(new_bid)
                bids = Bids.objects.filter(listing=listing)
                if bids.exists():
                    highest_bid = bids.order_by('-bid').first().bid
                    if new_bid > highest_bid:
                        bid = Bids(listing=listing, bid=new_bid, bidder=request.user)
                        bid.save()
                        listing.price = new_bid
                        listing.save() 
                        message = 'Bid Successful'
                    else:
                        message = f"Your bidding price must be higher than {highest_bid}"
                else:
                    if new_bid > listing.price:
                        bid = Bids(listing=listing, bid=new_bid, bidder=request.user)
                        bid.save()
                        listing.price = new_bid
                        listing.save()
                        message = 'Bid Successful'
                    else:
                        message = f'Your bidding price must be higher than {listing.price}'
            except ValueError:
                message = 'Invalid bid format. Please enter a number.'
        messages.success(request, message)
        return HttpResponseRedirect(reverse('auctions:listing', kwargs={'listing_id': listing_id}))
    else:
        return HttpResponseRedirect(reverse('auctions:listing', kwargs={'listing_id': listing_id}))

@login_required
def watchlist_action(request, listing_id):
    if request.method == 'POST' and 'watchlist' in request.POST:
        action = request.POST['watchlist']
        listing = get_object_or_404(AuctionListing, id=listing_id)
        listed_by = User.objects.filter(userwatchlist__listed=listing_id)
        
        if action == 'Remove from watchlist':
            watchlist = Watchlist.objects.filter(user=request.user, listed_id=listing_id)
            watchlist.delete()
            message = 'Removed from watchlist'
        else:
            watchlist = Watchlist(user=request.user, listed_id=listing_id)
            watchlist.save()
            message = 'Added to watchlist'
        messages.success(request, message)
        return HttpResponseRedirect(reverse('auctions:listing', kwargs={'listing_id': listing_id}))

    else:
        return HttpResponseRedirect(reverse('auctions:listing', kwargs={'listing_id': listing_id}))

@login_required
def toggle_auction(request, listing_id):
    if request.method == 'POST' and 'close auction' in request.POST:
        action = request.POST['close auction']
        listing = get_object_or_404(AuctionListing, id=listing_id)
        if action == 'Close Auction':
            listing.active = False
            listing.save()
            message = 'Auction Closed.'
        else:
            listing.active = True
            listing.save()
            message = 'Auction Opened'
        messages.success(request, message)
        return HttpResponseRedirect(reverse('auctions:listing', kwargs={'listing_id': listing_id}))
    else:
        return HttpResponseRedirect(reverse('auctions:listing', kwargs={'listing_id': listing_id}))

@login_required
def comment(request, listing_id):
    if request.method == 'POST' and 'comment' in request.POST:
        comment = request.POST['comment']
        user = request.user
        listing = get_object_or_404(AuctionListing, id=listing_id)
        new_comment = Comment(listing=listing, comment=comment, user=user)
        new_comment.save()
        
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={'listing_id': listing_id}))


def listing_page(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    current_user = request.user
    owner = User.objects.get(username=current_user.username)
    items_owned = owner.owner.all()
    listed_by = User.objects.filter(userwatchlist__listed=listing_id)  
    is_active = listing.active
    comments = Comment.objects.filter(listing=listing_id)
    bids = Bids.objects.filter(listing=listing)
    
    if bids.exists():
       highest_bid = bids.order_by('-bid').first().bid
       bid= Bids.objects.get(listing=listing_id, bid=highest_bid)
       winner = bid.bidder 
    else:
        winner = None
    
    
    return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'items_owned': items_owned,
        'is_active': is_active,
        'listed_by': listed_by,
        'comments': comments,
        'current_user': current_user,
        'winner': winner
    })


@login_required
def watchlist_page(request):
    user_watchlist= AuctionListing.objects.filter(listings__user=request.user)
    context = {'user_watchlist': user_watchlist}
    return render(request, "auctions/watchlist.html", context)

def categories(request):
    categories = Category.objects.all()
    context={'categories':categories}
    return render(request, "auctions/categories.html", context)

def category(request, category_id):
   listings= AuctionListing.objects.filter(category=category_id)
   context={'listings':listings}
   return render(request, "auctions/category.html", context)


    
  

