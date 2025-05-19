from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import cloudinary.api
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from PIL import Image
from users_sys.models import ShopProfile, CustomerProfile 
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime
import decimal

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
    
class Discounts(models.Model):

    product = models.ForeignKey("Products", on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.BooleanField(default=False)

    def is_active(self):
        today = timezone.localtime(timezone.now())
        print(f'''
        {today}
        Start date : {timezone.localtime(self.start_date)}
        End date : {timezone.localtime(self.end_date)}
        ''')
        if timezone.localtime(self.start_date) <= today <= timezone.localtime(self.end_date):
            print('True')
            self.status = True
        elif today >= timezone.localtime(self.end_date):
            print('delete')
            
            self.delete()
            
        else:
            print('false')
            self.status = False
        return self.status

    def __str__(self):
        return self.product.name

class Products(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2,)
    availability = models.BooleanField()
    character = models.TextField(default='')
    description = models.TextField(default='')
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, null=True, related_name='products')
    discount = models.ForeignKey(Discounts, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')

    @property
    def formatted_price(self):
        return f'{self.price:,.2f}'.replace(',', ' ').replace('.00', '')


    @property
    def has_active_discount(self):
        if self.discount != None:
            return self.discount.is_active
            
    @property
    def price_with_discount(self):
        if self.has_active_discount:
            return decimal.Decimal(float(self.price)  * (1 - self.discount.discount_percentage / 100))
        
        return self.price

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
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='review')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('add_review_who_but_it', 'Add review who buy it'),
        ]

    def __str__(self):
        return self.user.username

class Baskets(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')
    products = models.ManyToManyField(Products, related_name='basket')

    class Meta:
        permissions = [
            ('add_product_to_busket', 'Add product to busket'),
        ]

    def __str__(self):
        return self.user.username

class ItemBasket(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='item_basket')
    basket = models.ForeignKey(Baskets, on_delete=models.CASCADE)




class Orders(models.Model):
    STATUS_CHOICES = [
        ['framed','Замовлення оформлено'],
        ['transit', 'Доставляється' ],
        ['delivered', 'Доставлено'],
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


