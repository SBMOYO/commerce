from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Auction_listings,Bids, Watch_list, Comments, Category
from django import forms



class AuctionListingsForm(forms.ModelForm):
    class Meta:
        model = Auction_listings
        fields = ['item_name', 'price', 'discription', 'image', 'category', 'listed_by']


def index(request):
    listings = Auction_listings.objects.filter(is_active=True)
    categories = Category.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):

    if request.method == 'POST':
        form = AuctionListingsForm(request.POST, request.FILES)
        if form.is_valid():
            
           form.save()
           return HttpResponseRedirect(reverse('index'))
                       
    else:
        form = AuctionListingsForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })


@login_required
def listing(request, id):

    listing_item = Auction_listings.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    all_comments = Comments.objects.filter(item=id)
    
    
    try:
        bid_count = Bids.objects.filter(item=id).count()
        max_bid = Bids.objects.filter(item=id).aggregate(Max('bid'))['bid__max']
        max_bid_obj = Bids.objects.get(item=id, bid=max_bid)
        max_bidder = max_bid_obj.user
                 
    except ObjectDoesNotExist:
        bid_count = None
        max_bid = None
        max_bid_obj = None
        max_bidder = None

    creator = listing_item.listed_by == user
    winner = None

    if max_bidder == user:
        winner = max_bidder
    
    return render(request, "auctions/listing.html", {
        "listing_item": listing_item,
        "count": bid_count,
        "creator": creator,
        "max_bid": max_bid,
        "max_bidder": max_bidder,
        "winner": winner,
        "all_comments": all_comments
    })

@login_required
def watchlist(request):

    message = None
    color = None
    
    if request.method == "POST":
        item_id = request.POST['item_id']

        try:
            item = Auction_listings.objects.get(pk=item_id)
            if request.user.is_authenticated:
                watch_list, created = Watch_list.objects.get_or_create(item=item, user=request.user)
                if created:
                    # A new Watch_list object was created
                    message = "added to watchlist"
                    color = "p-3 text-success-emphasis bg-success border border-success rounded-3"
                else:
                    # An existing Watch_list object was found
                    message = "already exists in watchlist"
                    color = "p-3 text-danger-emphasis bg-danger-light border border-danger rounded-3"

        except Auction_listings.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))
        
    watch_list = Auction_listings.objects.filter(watch_list__user=request.user)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watch_list,
        "message": message,
        "color": color
    })

@login_required
def watchlist_del(request):
    if request.method == 'POST':
        id = request.POST['item_id']
        watch_list = Watch_list.objects.get(item=id, user=request.user.id)
        watch_list.delete()

        return HttpResponseRedirect(reverse('watchlist'))
    
@login_required
def bids(request):
    
    if request.method == "POST":
        if not request.POST['bid_price']:
            message = "Place a bid"
        else:
            item_bid = float(request.POST['bid_price'])
            id = int(request.POST['id'])
            max_bid = Bids.objects.filter(item=id).aggregate(Max('bid'))['bid__max']
            item = Auction_listings.objects.get(pk=id)
            user = User.objects.get(pk=request.user.id)

            if item.listed_by != user:

                if item_bid > item.price and (max_bid is None or item_bid > max_bid):
                    
                    Bids.objects.create(bid=item_bid, user=user, item=item)

                else:
                    return render(request, "auctions/listing.html", {"id":id})
                
            else:

                return HttpResponseRedirect(reverse("watchlist"))

    return HttpResponseRedirect(reverse('index'))

@login_required
def close_biding(request, id):
    alert = None
    the_winner = None
    color = None

    listing_item = Auction_listings.objects.get(pk=id)

    bid_count = Bids.objects.filter(item=id).count()
    max_bid = Bids.objects.filter(item=id).aggregate(Max('bid'))['bid__max']
    max_bid_obj = Bids.objects.get(item=id, bid=max_bid)
    max_bidder = max_bid_obj.user
    print(max_bidder)


    user = User.objects.get(pk=request.user.id)

    creator = listing_item.listed_by == user

    if request.method == "POST":
        #id = request.POST["close"]
        item = Auction_listings.objects.get(pk=id)
        item.is_active = False
        item.save()

        if item.is_active == False:
            alert = "Bid successfully closed!!!"
            color = "p-3 text-success-emphasis bg-success border border-success rounded-3"
            check_winner = max_bidder == user
            print(check_winner)
             

    return render(request, "auctions/listing.html", {
        "listing_item": listing_item,
        "alert": alert,
        "color": color,
        "count": bid_count,
        "creator": creator,
        "max_bid": max_bid,
        "check_winner": check_winner,
        "user": user
    })

@login_required
def comment(request, id):
    new_item = Auction_listings.objects.get(pk=id)
    new_user = request.user
    add_comment = request.POST['new_comment']

    new = Comments.objects.create(item=new_item, user=new_user, comment=add_comment)
    new.save()

    return HttpResponseRedirect(reverse("listing",args=(id, )))

def category(request):
    if request.method == "POST":
        cat = request.POST['category']
        cat = Category.objects.get(Category=cat)
        listings = Auction_listings.objects.filter(is_active=True, category=cat)
        categories = Category.objects.all()

        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories
        })
