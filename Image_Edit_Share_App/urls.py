from django.conf.urls import url
from Image_Edit_Share_App import views
urlpatterns = [
    # url(r'^sign_in/$', views.sign_in, name="sign_in"),
    # url(r'^log_in/$', views.log_in, name="log_in"),

    url(r'^profile_page/(?P<pk>\d+)$', views.profile_page, name="profile_page"),
    url(r'^edit_profile/$', views.edit_profile, name="edit_profile"),
    url(r'^uploadImage/$', views.upload_image, name="uploadImage"),
    url(r'^change_image/$', views.change_image, name="change_image"),
    url(r'^set_post_text/$', views.set_post_text, name="set_post_text"),
    # url(r'^download_image/$', views.download_image, name="download_image"),
    url(r'^delete_post/(?P<pk>\d+)$', views.delete_post, name="delete_post"),
    url(r'^change_black_white$', views.change_black_white, name="change_black_white"),
    url(r"^reset_image$", views.reset_image, name="reset_image"),
    url(r"^change_size_of_image$", views.change_size_of_image, name="change_size_of_image"),
    url(r"^change_contract_image$", views.change_contract_image, name="change_contract_image"),
    url(r"^add_score_image$", views.add_score_image, name="add_score_image"),
    url(r"^delete_comment$", views.delete_comment, name="delete_comment"),
    url(r"^approve_comment$", views.approve_comment, name="approve_comment"),
    url(r"^user_add_comment", views.user_add_comment, name="user_add_comment"),
]

