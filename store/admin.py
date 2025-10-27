from django.contrib import admin
from .models import product ,Customer,Cart,OrderPlaced

# Register your models here.
@admin.register(product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','category','image','title','discounted_price']
    
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','zipcode','state']
    
    




@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
 
 
 
@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'customer', 'ordered_date', 'status']
    list_filter = ['status', 'ordered_date']
    search_fields = ['user__username', 'product__title', 'customer__name']
    list_editable = ['status']  # Admin can change status directly from list
    
    
 