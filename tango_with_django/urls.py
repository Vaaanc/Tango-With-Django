"""tango_with_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings # New Import
from django.conf.urls.static import static # New Import
from registration.backends.simple.views import RegistrationView
from rango import views

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/rango/add_profile/'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rango/', include('rango.urls')),
    url(r'^accounts/register/', MyRegistrationView.as_view(), name='registration_register'),
    url('^accounts/', include('registration.backends.simple.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
