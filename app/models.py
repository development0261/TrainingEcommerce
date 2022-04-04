from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator




# Create your models here.

class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)

    def __str__(self):  
        return self.category_name

STATE_CHOICES = (('Gujarat','Gujarat'),
                 ('Maharastra','Maharastra'),
                 ('Rajasthan','Rajasthan'))

class Customer(models.Model):
    user      = models.ForeignKey(User,on_delete=models.CASCADE)
    name      = models.CharField(max_length=200)
    locality  = models.CharField(max_length=200)
    city      = models.CharField(max_length=50)
    zipcode   = models.IntegerField()
    phone     = models.CharField(max_length=11)
    state     = models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):  
        return self.name


class Product(models.Model):
    pid              = models.AutoField(primary_key=True)
    category         = models.ForeignKey(Category,on_delete=models.PROTECT)
    title            = models.CharField(max_length=100)
    selling_price    = models.FloatField()
    discounted_price = models.FloatField()
    description      = models.TextField()
    brand            = models.CharField(max_length=100)
    product_image    = models.ImageField(upload_to='productimage')

    def __str__(self):  
        return self.title

class Cart(models.Model):
    user      = models.ForeignKey(User,on_delete=models.CASCADE)
    product   = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity  = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])

    def __str__(self):  
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','One The Way'),
    ('Deliverd','Deliverd'),
    ('Cancel','Cancel'),
    ('Pending','Pending')
)


class OrderPlaced(models.Model):
     user      = models.ForeignKey(User,on_delete=models.CASCADE)
     customer  = models.ForeignKey(Customer,on_delete=models.CASCADE)
     product   = models.ForeignKey(Product,on_delete=models.PROTECT)
     quantity  = models.PositiveIntegerField(default=1)
     ordered_date = models.DateTimeField(auto_now_add=True)
     status    = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
     price     = models.FloatField(default=0.0)
     

     def __str__(self):
         return str(self.user)

     @property
     def total_cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
    user      = models.ForeignKey(User,on_delete=models.CASCADE)
    product   = models.ForeignKey(Product,on_delete=models.PROTECT)

    def __str__(self):  
        return str(self.id)