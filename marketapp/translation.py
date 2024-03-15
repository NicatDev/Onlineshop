from modeltranslation.translator import TranslationOptions,register, translator
from marketapp.models import Color,Size,Product,Category,Collection,Blog,BlogTag,Brand



class NameTranslationOption(TranslationOptions):
    fields = ('name',)


class ProductTranslationOption(TranslationOptions):
    fields = ('name','description','material')
  
class BlogTranslationOption(TranslationOptions):
    fields = ('title','content','content_without_ck','content2')


translator.register(Color, NameTranslationOption)
translator.register(Size, NameTranslationOption)
translator.register(Category, NameTranslationOption)
translator.register(BlogTag, NameTranslationOption)
translator.register(Collection, NameTranslationOption)
translator.register(Brand, NameTranslationOption)

translator.register(Product, ProductTranslationOption)
translator.register(Blog, BlogTranslationOption)
