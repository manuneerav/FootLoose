from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import *
from .forms import createuserform
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.decorators import login_required
import razorpay
# Create your views here.
def store(request):
    return render(request,'store.html')


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
            # items = []
            # order = {'Cart_Total':0,'Total_Items':0}
        context = {'items':items , 'order':order}
        return render(request,'cart.html',context)
    else:
        return render(request, 'login.html')

@login_required
def checkout(request):
    customer = request.user.customer
    order= Order.objects.get(customer = customer)
    items = order.orderitem_set.all()
    name = customer
    amount = order.Cart_Total*100
    client = razorpay.Client(auth=("rzp_test_QUldnLYWI6STEg","df2VK8OJZkiQFzt3PYzcIvgm"))
    payment = client.order.create({'amount':amount,'currency':'INR','payment_capture': '1'})
    order.transaction_id = payment['id']
    context = {'items':items , 'order':order,'payment':payment}
    return render(request,'checkout.html',context)
def base3(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'itempagetr.html',context)

def itempage(request,pk = None):
    if pk:
        if request.user.is_authenticated:
            product = Product.objects.get(pk = pk)
            print(123)
            customer = request.user.customer
            reviews = Reviews.objects.filter(product = product)
            rev = Reviews.objects.filter(customer=customer,product = product)
            print(rev)
            obj = Reviews.objects.filter(customer=customer,product = product,score=0).order_by("?").first()
            print(423)
            print(obj)
            recommend = Product.objects.filter(brand__icontains = product.brand)[0:5]
            context = {'product':product,'object':obj,'reviews':reviews,'rev':rev,'recommend':recommend}
        else:
            product = Product.objects.get(pk = pk)
            recommend = Product.objects.filter(brand__icontains = product.brand)[0:5]
            reviews = Reviews.objects.filter(product = product)
            context = {'product':product,'recommend':recommend}
    return render(request,'itempage.html',context)

def registerpage(request):
    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email= request.POST.get('email')
        user = User.objects.create_user(username, email,password)
        
        user.save()
        
        
        Customer.objects.create(user=user, name=username, email=user.email)
        context = {'user':user}
        return redirect('/loginpage')

    return render(request,'register.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Username or password is incorrect!')
    context = {}
    return render(request,'login.html',context)


def sports(request,pk = None):
    if pk:
        product = Product.objects.filter(category__icontains = pk)
        page = request.GET.get('page', 1)

        paginator = Paginator(product, 6)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request,'sports.html',{'products':products,'category':pk})
    else:
        product = Product.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(product, 6)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request,'sports.html',{'products':products})
def sports2(request,pk = None):
    if pk:
        product = Product.objects.filter(brand__icontains = pk)
        page = request.GET.get('page', 1)
        paginator = Paginator(product, 6)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request,'sports.html',{'products':products,'category':pk})

class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return super().default(o)

def search(request):
    pk1 = None
    if request.is_ajax():
        res = None
        name = request.POST.get('name')
        qs = Product.objects.filter(name__icontains = name)[0:5]
        if len(qs) > 0 and len(name)>0:
            data = []
            for pos in qs:
                result = json.dumps(pos.image, cls=ExtendedEncoder)
                item = {
                    'pk':pos.pk,
                    'name':pos.name,
                    'image':result,
                }
                data.append(item)
                pk1 = item["pk"]
            res = data
            resl = len(res)
            print("asdfvgbn",resl)
        else:
            resl = 0
            res = 'No names found'
        return JsonResponse({'data':res,'pk':pk1,})
    return JsonResponse({})


def add_to_cart(request,pk= None):
    if request.is_ajax():
        customer = request.user.customer
        m = Product.objects.get(id=pk)
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        orderitem,create = OrderItem.objects.get_or_create(order = order,product = m)
        orderitem.quantity +=1
        print(orderitem.pk)
        s = request.POST['size']
        print(s)
        orderitem.size = s
        order.save()
        orderitem.save()
        return JsonResponse({})
    else:return redirect('/itempage')


def quantity_update(request,pk = None):
    if request.is_ajax():
        orderitem = OrderItem.objects.get(id=pk)
        orderitem.quantity += 1
        orderitem.save()
        return JsonResponse({})
    else:
        return redirect('/cart')


def size(request,pk = None):
    if request.method == 'POST':
        s = request.POST['size']
        orderitem = OrderItem.objects.get(id=pk)
        orderitem.size = s
        orderitem.save()
        return JsonResponse({})
    else:
        return redirect('/cart')

def quantity_down(request,pk = None):
    if request.is_ajax():
        orderitem = OrderItem.objects.get(id=pk)
        if orderitem.quantity == 1:
            pass
        else:
            orderitem.quantity -= 1
            orderitem.save()
            return JsonResponse({})
    else:
        return redirect('/cart')
def removeitems(request,pk = None):
    if request.is_ajax():
        orderitem = OrderItem.objects.get(id=pk)
        orderitem.delete()
        return JsonResponse({})
    else:
        return redirect('/cart')

def logout_view(request):
    logout(request)
    return redirect('/')

def shippingadd(request):
    if request.is_ajax():
        customer = request.user.customer
        order= Order.objects.filter(customer = customer,complete=False).first()
        items = order.orderitem_set.all()
        shippingaddress,created = ShippingAddress.objects.get_or_create(customer = customer,order=order)
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        pincode = request.POST['pincode']
        shippingaddress.phone = phone
        shippingaddress.address = address
        shippingaddress.pincode = pincode
        name = customer
        amount = order.Cart_Total
        print(amount)
        client = razorpay.Client(auth=("rzp_test_QUldnLYWI6STEg","df2VK8OJZkiQFzt3PYzcIvgm"))
        payment = client.order.create({'amount':amount,'currency':'INR','payment_capture': '1'})
        print(payment)
        order.transaction_id = payment['id']
        order.save()
        shippingaddress.save()
        return JsonResponse(payment)
        # return JsonResponse({})
    else:return redirect('/checkout')

def rate_image(request):
    print(1234)
    if request.user.is_authenticated:
        if request.method == 'POST':
            el_id = request.POST.get('el_id')
            val = request.POST.get('val')
            print(val)
            print(el_id)

            obj = Reviews.objects.get(id=el_id)
            obj.score = val
            obj.save()
            return JsonResponse({'success':'true', 'score': val}, safe=False)
    return JsonResponse({'success':'false'})

# Review system
def review(request,pk=None):
    if request.is_ajax():
        if pk:
            print(24222222222222222222222222222222222222222222222222222222222222222222222)
            rev = request.POST.get('review')
            com = request.POST.get('comment')
            rt = request.POST.get('stay')
            customer = request.user.customer
            product = Product.objects.get(pk=pk)
            reviews,created = Reviews.objects.get_or_create(customer = customer,product=product)
            reviews.review = rev
            reviews.comment = com
            reviews.score = rt
            reviews.save()
            return JsonResponse({})


@csrf_exempt
def success(request):
    if request.method == 'POST':
        customer = request.user.customer
        order_id = ""
        a = request.POST
        for key,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        print(order_id)
        user = Order.objects.filter(customer=customer).first()
        user.complete = True
        user.delete()


        return redirect('/')
        