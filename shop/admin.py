from django.contrib import admin
from shop import models
# Register your models here.
admin.site.register(models.Baskets)
admin.site.register(models.Categories)
admin.site.register(models.Comment)
admin.site.register(models.Discounts)
admin.site.register(models.OrderItems)
admin.site.register(models.Orders)
admin.site.register(models.ProductImages)
admin.site.register(models.Reviews)
admin.site.register(models.Products)