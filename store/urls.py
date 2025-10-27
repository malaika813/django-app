
from django.urls import path,include
from . import views
from django.views import View
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm


urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path("category/<slug:val>/",views.category.as_view(),name="category"),
    path("product_detail/<int:pk>/",views.ProductDetail.as_view(),name="product_detail"),
    path("profile/",views.profile.as_view(),name="profile"),
    path("adress/",views.adress.as_view(),name="adress"),
    path("update_adress/<int:pk>/",views.update.as_view(),name="update_adress"),
    path("logout/", views.custom_logout, name="logout"),
    path("add-to-cart/", views.add_cart, name="add-to-cart"),
    path('cart/', views.cart, name='cart'),
    path("pluscart/", views.plus_cart, name="pluscart"),
    path("minuscart/", views.minus_cart, name="minuscart"),
    path("removecart/", views.remove_cart, name="removecart"),
     path('checkout/', views.checkout, name='checkout'),
      path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.orders, name='orders'),
    path('',include('book.urls')),
    
  
    
    
    
    
    
    
    
    
    #authentication
    path("Register/",views.CustomerRegistration.as_view(),name="Register"),
    path("accounts/login/",auth_views.LoginView.as_view(template_name="login.html" ,authentication_form=LoginForm),name='login'),


    
    
]+static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)
