from django.contrib import admin

# Register your models here.
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date')
    search_fields = ('title', 'content')

admin.site.register(News, NewsAdmin)
