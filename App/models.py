from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from App.choices import *


class CommonTimePicker(models.Model):
    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)
    class Meta:
        abstract = True

class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:    
            raise ValueError('Users must have an Email Address')
        user = self.model(
            email=self.normalize_email(email),
            is_active=False,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        if user.is_superuser:
            user.first_name = "Admin"
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser,CommonTimePicker):
    user_type = models.CharField("User Type", max_length=10, default="User",choices=USER_TYPE)
    email = models.EmailField("Email" , null=True, blank=True, unique=True,db_index=True)
    name = models.CharField("Name", max_length=256, blank=True, null=True)
    avatar = models.ImageField("profile photo", null=True, blank=True,upload_to='user_images')
    contact = models.IntegerField("contact", blank=True, null= True) 
    quantity = models.IntegerField("quantity",default=1, blank=True, null= True)
    any_suggestions = models.TextField("any suggestions", max_length=256, blank=True, null=True)

    is_superuser = models.BooleanField("Super User", default=False)
    is_staff = models.BooleanField("Staff", default=False)
    is_active = models.BooleanField("Active", default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def _str_(self):
        return f"{self.uuid}_{self.email}" 
    def has_perm(self, perm, obj=None):
        return self.is_staff
    def has_module_perms(self, app_label):
        return self.is_superuser
    def get_short_name(self):
        return self.email

class ProductModel(CommonTimePicker):
    title = models.CharField("Title",max_length=100, null=True,blank=True)
    disc = models.CharField("Disc",max_length=1000, null=True,blank=True)
    product_image = models.ImageField(upload_to='images/')
    category = models.CharField("Category",max_length=20, default='All', choices=CATEGORY)
    price = models.PositiveIntegerField("Price",default=0, blank=True, null=True)
    language = models.CharField("language", max_length=25, blank=True, null=True,choices=LANGUAGE)
    def __str__(self):
        return self.title

class CartUser(CommonTimePicker):  
    Cart_link = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="cart_link")
    title = models.CharField("Title",max_length=100, null=True,blank=True)
    disc = models.CharField("Disc",max_length=1000, null=True,blank=True)
    product_image = models.ImageField("Product Image", null=True, blank=True,upload_to='product_image')
    category = models.CharField("Category",max_length=20, null=True,blank=True)
    price = models.PositiveIntegerField("Price",default=0, blank=True, null=True)
    qty = models.PositiveIntegerField("Quantity",default=1, blank=True, null=True)