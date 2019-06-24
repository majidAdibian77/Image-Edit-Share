from django.contrib import admin
from Image_Edit_Share_App.models import PostModel, CommentPostModel, UserProfileInfo, Users_give_score

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(PostModel)
admin.site.register(CommentPostModel)
admin.site.register(Users_give_score)