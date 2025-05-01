from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import cloudinary.api
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from PIL import Image
from users_sys.models import ShopProfile, CustomerProfile 


cloudinary.config( 
    cloud_name = "den9yj6z5", 
    api_key = "498996848524315", 
    api_secret = "kWT8gvHt4tffDaRQPqv0SADQ5bE", # Click 'View API Keys' above to copy your API secret
    secure=True
)


FILE_UPLOAD_MAX_MEMORY_SIZE = 300 * 300 * 10

def file_validation(file):
    if not file:
        raise ValidationError("No file selected.")

    # For regular upload, we get UploadedFile instance, so we can validate it.
    # When using direct upload from the browser, here we get an instance of the CloudinaryResource
    # and file is already uploaded to Cloudinary.
    # Still can perform all kinds on validations and maybe delete file, approve moderation, perform analysis, etc.
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 10MB.")


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.username

class Products(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.IntegerField()
    availability = models.BooleanField()
    character = models.TextField(default='')
    description = models.TextField(default='')
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_images')
    image =  CloudinaryField('image', validators=[file_validation])
    
    
    is_primary = models.BooleanField()

    def __str__(self):
        return self.product.name
    
    

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.user.username

class Baskets(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')
    products = models.ManyToManyField(Products, related_name='basket')

    def __str__(self):
        return self.user.username

class Discounts(models.Model):

    STATUS_CHOICES = [
        ['Активна', 'activate'],
        ['Неактивна','deactivate']
    ]

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.product.name

class Orders(models.Model):
    STATUS_CHOICES = [
        ['framed','Замовлення оформлено'],
        ['transit', 'Доставляється' ],
        ['delivered', 'Доставлено'],
        ['received' ,'Отримано'],
        ['canceled', 'Скасовано'],
    ]

    user = models.ForeignKey(User, models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='framed')
    total_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
class OrderItems(models.Model):
    
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


