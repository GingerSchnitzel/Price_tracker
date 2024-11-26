from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .extended_views.register import register
from .extended_views.login import login_view
from .extended_views.add_product import add_product
from .extended_views.graph import product_price_graph
from .extended_views.home import home
from .extended_views.contact import contact_view
from .extended_views.about_us import about_us
from .extended_views.product_manage import toggle_notify, delete_product
from django.contrib.auth.views import LogoutView
from .views import main_view


urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    #path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('add_product/', add_product, name='add_product'),
    path('graph/', product_price_graph, name='price_graph'),
    path('contact/', contact_view, name='contact'),
    path('about-us/', about_us, name='about_us'),
    path('', main_view, name= 'main_view'),
    path('toggle_notify/', toggle_notify, name='toggle_notify'),
    path('delete_product/',delete_product, name='delete_product'),
    # urls.py
]



    



