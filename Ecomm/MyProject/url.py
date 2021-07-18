from django.urls import path,include
from MyProject import views

app_name = 'mp'

urlpatterns = [
    path('',views.store,name = 'store'),
    path('cart/',views.cart,name = 'cart'),
    path('checkout/',views.checkout,name = 'checkout'),
    path('base3/<str:pk>/',views.base3,name = 'base3'),
    path('itempage/',views.itempage,name = 'itempage'),
    path('itempage/<str:pk>/',views.itempage,name = 'itempage_pk'),
    path('registerpage/',views.registerpage,name = 'registerpage'),
    path('loginpage/',views.loginpage,name = 'loginpage'),
    path('sports/',views.sports,name = 'sports'),
    path('sports/<str:pk>/',views.sports,name = 'sports'),
    path('sports2/<str:pk>/',views.sports2,name = 'sports2'),
    path('s/',views.search,name = 'search'),
    path('add_to_cart/<str:pk>/',views.add_to_cart,name = 'updateitem'),
    path('quantity_update/<str:pk>/',views.quantity_update,name = 'quantity_update'),
    path('quantity_down/<str:pk>/',views.quantity_down,name = 'quantity_down'),
    path('removeitems/<str:pk>/',views.removeitems,name = 'removeitems'),
    path('size/<str:pk>/',views.size,name = 'size'),
    path('shippingadd/',views.shippingadd,name = 'shippingadd'),
    # path('a/',views.a,name = 'a'),
    # path('ratethestar/<str:pk>/',views.ratethestar,name = 'ratethestar'),
    path('removeitems/',views.removeitems,name = 'removeitems'),
    path('logout_view/',views.logout_view,name = 'logout_view'),
    path('review/<str:pk>/',views.review,name = 'review'),
    path('rate/',views.rate_image, name = 'rate'),
    path('success/',views.success, name = 'success'),
]
