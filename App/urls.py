from django.urls import path
from App.views import *
from .views import AddToCart


urlpatterns = [
     path("",LoginView.as_view(), name="login"),
     path("signup/",Signup.as_view(), name="signup"),
     path("dashboard/",Dashboard.as_view(),name="dashboard"),
     path("main-page/",MainPage.as_view(),name="main-page"),
     path("edit-user/<int:id>/",EditUser.as_view(),name="edit-user"),
     path("delete-user/<int:id>/",DeleteUser.as_view(),name="delete-user"),
     path("cart-details/",CartDetails.as_view(),name="cart-details"),
     path("check-out/",CheckOut.as_view(),name="check-out"),
     path("product/",ProductView.as_view(),name="product"),
     path("add-to-cart/<int:id>/",AddToCart.as_view(),name="add-to-cart"),
]