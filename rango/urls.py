from django.conf.urls import url
from . import views

app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^about/', views.about, name = 'about'),
    url(r'^category/(?P<slug>[\w\-]+)/$', views.category, name = 'category'),
    url(r'^add_category/', views.add_category, name = 'add_category'),
    url(r'^(?P<slug>[\w\-]+)/add_page/', views.add_page, name = 'add_page'),
    url(r'^register/', views.register, name = 'register'),
    url(r'^login/', views.login_user, name = 'login'),
    url(r'^restricted/', views.restricted, name = 'restricted'),
    url(r'^logout/', views.user_logout, name = 'logout'),
    url(r'^search/', views.search, name = 'search'),
    url(r'^goto', views.track_url, name = 'goto'),
    url(r'^add_profile/', views.register_profile, name = 'register_profile'),
    url(r'^profile/(?P<username>\D+)/$', views.profile_page, name = 'profile_page'),
    url(r'^profile/edit', views.edit_profile, name = 'edit_profile'),
    url(r'^like_category/$', views.like_category, name = 'likes_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
    url(r'^auto_add_page/$', views.auto_add_page, name='auto_add_page'),
]
