from re import template
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import MyPasswordChangeForm

urlpatterns = [
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('cart/',views.show_cart,name='showcart'),

    #pluse cart
    path('pluscart/',views.plus_cart),

    #minus cart
    path('minuscart/',views.minus_cart),

    #remove From cart
    path('removecart/',views.removecart),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('shirt/', views.shirts, name='shirt'),
    path('shirt/<slug:data>', views.shirts, name='shirtsdata'),
    path('jeans/', views.jeans, name='jeans'),
    path('jeans/<slug:data>', views.jeans, name='jeansdata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('login/', views.login_customer, name='login'),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone',views.paymentdone,name='paymentdone'),

    path('logout/', views.logout_customer, name='logout'),
    path('wishlist/',views.wish_list,name='wishlist'),
    path('addtowishlist/',views.addto_wishlist,name='addwishlist'),

    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name="passwordchange"),
    
    path('passwordchangedone',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name="passwordchangedone"),

]
