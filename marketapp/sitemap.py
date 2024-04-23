from django.contrib.sitemaps import Sitemap
from marketapp.models import *
from django.urls import reverse, NoReverseMatch


class BlogSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.6
    protocol = 'https'
    
    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj: Blog) -> str:
        return obj.get_absolute_url()

class ProductSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.6
    protocol = 'https'
    
    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj: Product) -> str:
        return obj.get_absolute_url()

class StaticSitemap(Sitemap):
    protocol = 'https'
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
            'home', 'about', 'shop',
            'blogs',  'contact',
        ]

    def location(self, item):
        try:
            return reverse(item)
        except NoReverseMatch:
            return reverse('home')

