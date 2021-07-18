from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=100,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100,null=True)
    price = models.FloatField()
    discription = models.TextField(max_length=500,null=True)
    image = models.ImageField(null=True,blank = True)
    category = models.CharField(max_length=100,null=True)
    starrate = models.IntegerField(null=True)
    brand = models.CharField(max_length=100,null=True)
    discount = models.IntegerField(null=True)
    def __str__(self):
        return self.name
    @property
    def newT(self):
        newPrice = self.price-((self.price*self.discount)//100)
        return newPrice

    @property
    def str_rating(self):
        i = 1
        reviews = self.reviews_set.all()
        rt = sum([rev.score for rev in reviews])
        num = sum([i for r in reviews])
        if rt != 0:
            rtng = (rt//num)
            return rtng
        else:return 1


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateField(auto_now=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.id)

    @property
    def Cart_Total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.Total for item in orderitems])
        return total

    @property
    def Total_Items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def Savings(self):
        orderitems = self.orderitem_set.all()
        savings = sum([(item.OldTotal-item.Total) for item in orderitems])
        return savings


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    size = models.IntegerField(default=9,null=True,blank=True)
    date_added = models.DateField(auto_now=True)

    @property
    def Total(self):
        total = self.product.newT * self.quantity
        return total
    @property
    def OldTotal(self):
        oldtotal = self.product.price * self.quantity
        return oldtotal


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=200,null=True)
    date_added = models.DateField(auto_now=True)
    phone = models.IntegerField(default=9999999999)
    # def __str__(self):
    #     return self.address\


class Reviews(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    review = models.TextField(max_length=200,null=True)
    date = models.DateField(auto_now=True)
    comment = models.CharField(max_length=100,null=True)
    score = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )


    def __str__(self):
        return str(self.product)
