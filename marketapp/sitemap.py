# from django.contrib.sitemaps import Sitemap
# from marketapp.models import *
# from django.urls import reverse, NoReverseMatch


# class BlogSiteMap(Sitemap):
#     changefreq = "daily"
#     priority = 0.6
#     protocol = 'https'
    
#     def items(self):
#         return Blog.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at
    
#     def location(self, obj: Blog) -> str:
#         return obj.get_absolute_url()
    
# class PortfolioSiteMap(Sitemap):
#     changefreq = "daily"
#     priority = 0.6
#     protocol = 'https'
    
#     def items(self):
#         return Portfolio.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at
    
#     def location(self, obj: Portfolio) -> str:
#         return obj.get_absolute_url()


# class TagSiteMap(Sitemap):
#     changefreq = "daily"
#     priority = 0.6
#     protocol = 'https'
    
#     def items(self):
#         return Tag.objects.all()

#     def location(self,item):
#         return reverse('home')
    
# class ServiceSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.6

#     def items(self):
#         return Services.objects.all()

#     def location(self, obj: Services) -> str:
#         return obj.get_absolute_url()
    
# class PortfolioCategorySitemap(Sitemap):
#     changefreq = "monthly"
#     priority = 0.6

#     def items(self):
#         return Portfolio_category.objects.all()
    
#     def location(self):
#         return reverse('home')


# class StaticSitemap(Sitemap):

#     priority = 0.5
#     changefreq = "daily"

#     def items(self):
#         return [
#             'home', 'about', 'services',
#             'blogs', 'portfolio',  'contact',
#         ]

#     def location(self, item):
#         try:
#             return reverse(item)
#         except NoReverseMatch:
#             # Eğer reverse işlemi başarısız olursa, hata durumuyla başa çıkabilirsiniz.
#             return reverse('home')

