"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from posixpath import join
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from article.views import article_list

urlpatterns = [
    path('', article_list, name='home'),
    path('admin/', admin.site.urls),

    # article
    path('article/', include('article.urls', namespace='article')),
    # user
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    # password reset
    path('password-reset/', include('password_reset.urls')),
]
# 给图片配置URL路径
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
