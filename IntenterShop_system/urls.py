"""
URL configuration for IntenterShop_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from shop.views import HomeView
from django.conf.urls.static import static
from . import settings

from django.views.decorators.cache import cache_page
from IntenterShop_system.settings import DEBUG

urlpatterns = [
    path('' , (cache_page(60*2))(HomeView.as_view()), name='home'),
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('auth/', include('users_sys.urls')),
    path('customer/', include('customer.urls')),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

if DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]