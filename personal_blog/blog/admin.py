from django.contrib import admin
from blog.models import Category, Comment, Post, PostImage
from . import models
from django.contrib import messages

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class BlogAdminArea(admin.AdminSite):
    site_header = "Blog Database For Moderators"

class TestAdminPermissions(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if request.user.groups.filter(name='blogerzy').exists():
            return True

        return True

    def has_delete_permission(self, request, obj=None):
        if obj != None and request.POST.get('action') == 'delete_selected':
            messages.add_message(request, messages.ERROR,(
                "Jestes pewien?"
            ) )
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_view_permission(self, request, obj=None):
        return True

        
blog_site = BlogAdminArea(name="BlogModerator")

blog_site.register(models.Post, TestAdminPermissions)
blog_site.register(Category, CategoryAdmin)
blog_site.register(Comment, CommentAdmin)
blog_site.register(PostImage, CommentAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostImage, CommentAdmin)