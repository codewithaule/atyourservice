from django.conf import settings
from django.conf.urls.static import static
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.urls import path, include  

from .sitemaps import CategorySitemap, PostSitemap



from bit.views import frontpage, about, robots_txt
from core.views import IndexPageView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexPageView.as_view(), name='index'),

    path('accounts/', include('allauth.urls')),

    path('about/', about, name='about'),
    path('', include('core.urls')),
    path('', frontpage, name='frontpage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)