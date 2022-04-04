from django.contrib import admin
from .models import Category,Customer,Product,Cart,OrderPlaced,Wishlist

# Register your models here.

class Cartadmin(admin.ModelAdmin):
    list_display  = ('user','product','quantity')

class Productadmin(admin.ModelAdmin):
    list_display = ('pid','category','title','selling_price','discounted_price','description','brand')

class Categoryadmin(admin.ModelAdmin):
    list_display = ('cid','category_name')

class Customeradmin(admin.ModelAdmin):
    list_display = ('user','name','locality','city','zipcode','state')

class OrderPlacedadmin(admin.ModelAdmin):
    list_display = ('user','customer','product','quantity','ordered_date','status','price')

admin.site.register(Category,Categoryadmin)
admin.site.register(Customer,Customeradmin)
admin.site.register(Product,Productadmin)
admin.site.register(Cart,Cartadmin)
admin.site.register(OrderPlaced,OrderPlacedadmin)
admin.site.register(Wishlist)
