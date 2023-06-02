from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_del", views.watchlist_del, name="watchlist_del"),
    path("bids", views.bids, name="bids"),
    path("close_biding/<int:id>", views.close_biding, name="close_biding")
]
