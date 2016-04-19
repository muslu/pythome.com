import debug_toolbar
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from hatalar.views import anasayfa, hatabul, detaygoster

urlpatterns = [

    url(r'^$', anasayfa),
    url(r'^hatabul/', hatabul),
    url(r'^([\w\-]+)/([\w\-]+)/([\w\-]+)/$', detaygoster),

    # url(r'^ara/', otomatiksonuc, name='get_drugs'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),


    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^admin/', admin.site.urls),
]




# CREATE TABLE `Hatalar` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `Dosyayolu` varchar(250) NOT NULL,
#   `SatirSayisi` varchar(6) NOT NULL,
#   `Modul` varchar(20) NOT NULL,
#   `HataTuru` varchar(50) NOT NULL,
#   `HataFull` text NOT NULL,
#   `HataEng` text NOT NULL,
#   `Aciklama` text,
#   `Slug` varchar(250) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=694 DEFAULT CHARSET=utf8
#
