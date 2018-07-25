from django.conf.urls import url
from . import views  
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^home$', views.home, name='home'),
    url(r'^add_quote$', views.add_quote, name='add_quote'),
    url(r'^edit_account$', views.edit_account, name='edit_account'),
    url(r'^show_edit_account$', views.show_edit_account, name='show_edit_account'),
    url(r'^(?P<id>\d+)/show_user$', views.show_user, name='show_user'),
    url(r'^(?P<id>\d+)/destroy$', views.destroy, name='destroy'),
    url(r'(?P<id>\d+)/create_like$', views.create_like, name='create_like'),
]                            
