from django.contrib import admin
from blog.models import Category, Post, PostImage, Comment, Youtube
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'status']
    list_filter = ['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_posts_count', 'related_posts_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Post,
                'category',
                'posts_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Post,
                 'category',
                 'posts_count',
                 cumulative=False)
        return qs

    def related_posts_count(self, instance):
        return instance.posts_count
    related_posts_count.short_description = 'related article(category)'

    def related_posts_cumulative_count(self, instance):
        return instance.posts_cumulative_count
    related_posts_cumulative_count.short_description = 'related article(total categories)'

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class CommentAdmin(admin.ModelAdmin):
    list_display = ['status', 'subject', 'comment', 'post', 'created_at']
    list_filter = ['status']
    readonly_fields = ('subject', 'comment', 'ip', 'user', 'post', 'parent')

class YoutubeInline(admin.TabularInline):
    model = Youtube
    extra = 1

class YoutubeAdmin(admin.ModelAdmin):
    list_display = ['post', 'video']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [PostImageInline, YoutubeInline]
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Category, CategoryAdmin2)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostImage)
admin.site.register(Youtube, YoutubeAdmin)