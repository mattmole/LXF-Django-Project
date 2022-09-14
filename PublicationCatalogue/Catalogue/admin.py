from django.contrib import admin

from .models import Publisher,Publication,Edition,Article,Author,Tag

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('publicationName', 'publisher', 'publicationType')

class TagAdmin(admin.ModelAdmin):
    list_display = ('tagName', 'tagDescriptor')

class EditionAdmin(admin.ModelAdmin):
    list_display = ('editionName', 'publicationDate', 'publication')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('articleName', 'keywords', 'notes','summary')

admin.site.register(Publisher)
admin.site.register(Publication,PublicationAdmin)
admin.site.register(Edition,EditionAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Author)
admin.site.register(Tag,TagAdmin)
