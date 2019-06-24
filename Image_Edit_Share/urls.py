"""Image_Edit_Share URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from Image_Edit_Share_App import views
from django.contrib.auth import views as djangoView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url('admin/', admin.site.urls),
                  url(r'^$', views.home, name="home"),
                  url(r'^login/$', djangoView.LoginView.as_view(), name="login"),
                  url(r'^logout/$', djangoView.LogoutView.as_view(), name="logout"),
                  url(r'^register/$', views.register, name='register'),
                  url(r'', include("Image_Edit_Share_App.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
