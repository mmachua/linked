from django.conf.urls import url
from django.urls import include, re_path
from home.views import HomeView, CreateView,AboutView, Post_detailView, PostFormView , ProfileUpdateView, MemeLordsView, load_more_posts#, ContactView
from django.contrib.auth import views as auth_views
from . import views as myapp_views
#from home.forms import PostForm
from home import views
from . import views 

app_name = 'home'
urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path('load_more_posts/', views.load_more_posts, name='load_more_posts'),
    re_path(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', 
            views.change_friends, name='change_friends'),
    re_path(r'^like/$', views.like_post, name='like_post'),

    re_path(r'^create/$', CreateView.as_view(), name='create'),
   
    re_path(r'^about/$', AboutView.as_view(), name='about'),
    
    re_path(r'contact/$', views.contact, name='contact'),

    re_path('post/', PostFormView.as_view(), name = 'post'),

    re_path(r'^(?P<id>\d+)/$', Post_detailView.as_view(), name='post_detail'),
    re_path('updateprofile/', ProfileUpdateView.as_view(), name='updateprofile'),
    re_path('memelords/', MemeLordsView.as_view(), name='memelords'),
   
]