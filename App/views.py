from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from App.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import ProductModel, CartUser


class LoginView(View):
    def get(self, request):
        print("i am working check ")
        return render(request, "login.html")
    def post(self, request):
        print("==",request.POST)
        user = authenticate(email=request.POST.get("email"),password=request.POST.get("password"))
        print(user)
        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:  
            return redirect("login")  


class Signup(View):
    def get(self, request):
        return render(request, "signup.html")
    def post(self, request):
        print("==",request.POST)
        hashed_password = make_password(request.POST.get("password"))
        if MyUser.objects.filter(email=request.POST.get("email")).exists():
            return redirect("signup")
        MyUser(user_name=request.POST.get("name"),
            email=request.POST.get("email"), 
            password=hashed_password,
            is_superuser=True,
            is_staff=True, 
            is_active=True).save()
        return redirect("dashboard")


class Dashboard(View):
    def get(self, request):
        data = MyUser.objects.all()
        return render(request, "dashboard.html")


class MainPage(View):
    def get(self, request):
        data = ProductModel.objects.all()
        return render(request, "main-page.html",{"data":data})
    def post(self, request):
        if MyUser.objects.filter(email=request.POST.get("email_address")).exists():
            return redirect("main-page")
        else:
            data = MyUser(name=request.POST.get("name"),
                email=request.POST.get("email_address"),
                contact=request.POST.get("contact"),
                quantity=request.POST.get("quantity"),
                any_suggestions=request.POST.get("any_suggestions")
                )
            data.save()     
        return redirect("product")


class EditUser(View):
    def get(self, request, id):
        obj = MyUser.objects.get(id=id)
        return render(request, "edit-user.html",{"data":obj}) 
    def post(self, request, id):
        data = MyUser.objects.get(id=id)
        data.name = request.POST.get("name")
        data.email = request.POST.get("email_address")
        data.contact = request.POST.get("contact")
        data.quantity = request.POST.get("quantity") 
        data.language = request.POST.get("language") 
        data.any_suggestions = request.POST.get("any_suggestions") 
        data.save()
        return redirect("main-page")


class DeleteUser(View):
    def get(self, request, id):
        del_obj = MyUser.objects.get(id=id)
        del_obj.delete()
        return redirect("check-out")     


class CheckOut(View):
    def get(self, request):
        return render(request, "check-out.html")   


class CartDetails(View):
    def get(self, request):
        user = request.user
        cart_items = ProductModel.objects.filter(user=user)
        context = {
            'cart_items': cart_items
        }
        return render(request, "cart-details.html", context)     
    
class ProductView(View):
    def get(self, request):
        data = ProductModel.objects.all()   
        return render(request, "product.html",{"data":data})
    def product_view(request):
    # Adjust this as necessary to get the correct product
        product = get_object_or_404(product, id= id)  
        return render(request, "product.html", {"product": product})
    
class AddToCart(View):
    def get(self, request, id):
        obj = ProductModel.objects.get(id=id)
        cart_items = CartUser.objects.filter(Cart_link=request.user)
        return render(request, "cart-details.html", {"obj": obj, "cart_items": cart_items})
    def post(self, request, id):
        product_id = request.POST.get("product_id")
        product = get_object_or_404(ProductModel, id=product_id)
        CartUser.objects.create( 
            Cart_link=request.user,
            title=product.title,
            price=product.price,
            product_image=product.product_image,
            category=product.category)
        return redirect("cart-details")