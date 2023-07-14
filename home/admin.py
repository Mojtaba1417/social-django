from django.contrib import admin
from . models import Post, Comment

# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'updated', 'published')
    list_filter = ('published', )
    search_fields = ('slug', 'body')
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('user', )


admin.site.register(Comment)
# admin.site.register(Post, PostAdmin)
