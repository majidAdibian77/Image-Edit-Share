import os
from PIL import Image, ImageEnhance
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from Image_Edit_Share_App.forms import UserForm, UserProfileInfoForm, PostForm
from Image_Edit_Share_App.models import UserProfileInfo, PostModel, Users_give_score, CommentPostModel
# Create your views here.

"""
This method renders home page
"""


def home(request):
    hash = {}
    posts = PostModel.objects.all().order_by("-post_time")
    top_users = UserProfileInfo.objects.all().order_by("-score")[:5]
    hash["posts"] = posts
    hash["top_users"] = top_users
    return render(request, "mainPages/home.html", hash)


def contact_us(request):
    top_users = UserProfileInfo.objects.all().order_by("-score")[:5]
    return render(request, "mainPages/contact_us.html", {'top_users': top_users})


""" 
This method is for user registering
"""


def register(request):
    top_users = UserProfileInfo.objects.all().order_by("-score")[:5]
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            auth_user = authenticate(username=user_form.cleaned_data.get('username'),
                                     password=user_form.cleaned_data.get('password1'))
            login(request, auth_user)
            return redirect("profile_page", pk=user.id)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, "registration/register.html",
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'top_users': top_users})


#
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect("/")

"""
This method renders page to show profile and posts of user
"""


def profile_page(request, pk):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    users_info = UserProfileInfo.objects.filter(user=user)
    """""
        This "if" is for when user is admin so he has not profile. 
    """""
    if users_info:
        user_info = users_info[0]
        user_posts = PostModel.objects.filter(user=user).order_by("post_time")
        if user_posts:
            path = user_posts[0].image.url
            path = path[1:]
            new_path1 = path[:path.rfind('.')] + "_new1" + path[path.rfind('.'):]
            new_path2 = path[:path.rfind('.')] + "_new2" + path[path.rfind('.'):]
            if os.path.exists(new_path1):
                os.remove(path)
                os.renames(new_path1, path)
            if os.path.exists(new_path2):
                os.remove(path)
                os.renames(new_path2, path)

        return render(request, "mainPages/profile_page.html", {"user_info": user_info, "user_posts": user_posts})
    else:
        return redirect("home")


"""
This method is for editing profile of user
"""


def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_form.username = request.user.username
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user.username = user_form.cleaned_data.get("username")
            user.set_password = user_form.cleaned_data.get("password1")
            user.first_name = user_form.cleaned_data.get("first_name")
            user.last_name = user_form.cleaned_data.get("last_name")
            user.save()

            profile = UserProfileInfo.objects.get(user=user)
            profile.user = user
            profile.bio = profile_form.cleaned_data.get("bio")

            if 'profile_pic' in request.FILES:
                delete_image_profile(user)
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            auth_user = authenticate(username=user_form.cleaned_data.get('username'),
                                     password=user_form.cleaned_data.get('password1'))
            login(request, auth_user)
            return redirect("profile_page", pk=user.id)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        user = User.objects.get(pk=request.user.id)
        user.username = user.username + "_username_is_changed"
        user.save()
    return render(request, "registration/register.html",
                  {'user_form': user_form,
                   'profile_form': profile_form})


"""
This method is for delete image of profile that user remove it from database
"""


def delete_image_profile(user):
    img = UserProfileInfo.objects.get(user=user)
    path = img.profile_pic.url[1:]
    if os.path.exists(path):
        os.remove(path)
    path2 = path[:path.rfind('.')] + "_new1" + path[path.rfind('.'):]
    if os.path.exists(path2):
        os.remove(path2)
    path3 = path[:path.rfind('.')] + "_new2" + path[path.rfind('.'):]
    if os.path.exists(path3):
        os.remove(path3)
    img.delete()


"""
This method renders page to show form of upload image of post
"""


@login_required
def upload_image(request):
    upload_form = PostForm()
    error = ""
    if request.method == "POST":
        upload_form = PostForm(data=request.POST)
        if upload_form.is_valid():
            image_form = upload_form.save(commit=False)
            image_form.user = request.user
            if 'image' in request.FILES:
                image_form.image = request.FILES['image']
                image_form.save()
                return redirect("change_image")
        error = "There is a problem in uploading!!"
    return render(request, "editImage/uploadImage.html", {"form": upload_form, "error": error})


"""
This method is called from js file to set post text to related post in data base
"""


def set_post_text(request):
    post_text = request.GET.get("post_text", None)
    post_pk = request.GET.get("post_pk", None)
    post = PostModel.objects.get(pk=post_pk)
    post.text = post_text
    post.set_post_time()
    post.save()
    data = {
    }
    return JsonResponse(data)


"""
This method renders page of edit image of post
"""


@login_required
def change_image(request):
    hash = {}
    image = PostModel.objects.filter(user=request.user).order_by("-post_time")[0]
    hash["img"] = image
    hash["user"] = request.user
    path = image.image.url
    img = Image.open(path[1:])
    width = img.size[0]
    height = img.size[1]
    if width > 500:
        width = 500
    elif width < 200:
        width = 200
    if height > 600:
        height = 600
    elif height < 300:
        height = 300
    size = (width, height)
    temp_img = img.resize(size, Image.ANTIALIAS)
    temp_img.save(path[1:])

    """"
        Remove changed image if it exists after refreshing page
    """
    path2 = path[:path.rfind('.')] + "_new1" + path[path.rfind('.'):]
    if os.path.exists(path2):
        os.remove(path2)
    path3 = path[:path.rfind('.')] + "_new2" + path[path.rfind('.'):]
    if os.path.exists(path3):
        os.remove(path3)
    return render(request, "editImage/editImage.html", hash)


"""
This method is for delete image of post that user remove it from database
"""


def delete_image_post(pk):
    img = PostModel.objects.get(pk=pk)
    path = img.image.url[1:]
    if os.path.exists(path):
        os.remove(path)
    path2 = path[:path.rfind('.')] + "_new1" + path[path.rfind('.'):]
    if os.path.exists(path2):
        os.remove(path2)
    path3 = path[:path.rfind('.')] + "_new2" + path[path.rfind('.'):]
    if os.path.exists(path3):
        os.remove(path3)
    img.delete()


"""
This method is for delete post from database
"""


def delete_post(request, pk):
    delete_image_post(pk)
    return redirect("profile_page", pk=request.user.id)


"""
This method is called from js file to change image of post to black_white 
"""


def change_black_white(request):
    general_image_url = request.GET.get("general_image_url", None)
    new_image_url = request.GET.get("new_image_url", None)
    if not os.path.exists(new_image_url[1:]):
        new_image_url = general_image_url
    image_file = Image.open(new_image_url[1:])  # open colour image
    image_file = image_file.convert('L')  # convert image to black and white

    new_image_url1 = general_image_url[:general_image_url.rfind('.')] + "_new1" + general_image_url[
                                                                                  general_image_url.rfind('.'):]
    new_image_url2 = general_image_url[:general_image_url.rfind('.')] + "_new2" + general_image_url[
                                                                                  general_image_url.rfind('.'):]
    if os.path.exists(new_image_url1[1:]):
        os.remove(new_image_url1[1:])
        new_image_url = new_image_url2
    else:
        if os.path.exists(new_image_url2[1:]):
            os.remove(new_image_url2[1:])
        new_image_url = new_image_url1
    image_file.save(new_image_url[1:])
    data = {
        "newImage_url": new_image_url
    }
    return JsonResponse(data)


"""
This method is called from js file to reset all changes on image in post
"""


def reset_image(request):
    image_url = request.GET.get("image_url", None)
    path = image_url[1:]
    os.remove(path=path)
    new_image_url = image_url[:(image_url.rfind('_'))] + image_url[(image_url.rfind('.')):]
    img = Image.open(new_image_url[1:])
    width = img.size[0]
    height = img.size[1]
    if width > 500:
        width = 500
    elif width < 200:
        width = 200
    if height > 600:
        height = 600
    elif height < 300:
        height = 300
    data = {
        "newImage_url": new_image_url,
        "width": width,
        "height": height
    }
    return JsonResponse(data)


"""
This method is called from js file to changes size of image in post
"""


def change_size_of_image(request, pk):
    image_url = request.GET.get("image_url", None)
    width = int(request.GET.get("width", None))
    height = int(request.GET.get("height", None))
    user = User.objects.get(pk=pk)
    user = UserProfileInfo.objects.filter(user=user)[0]
    type_user = str(user.typeOfUser)
    """
    This "if" is to limit resizing image for different types of user
    1280*720  for simple
    1980*1080  for silver
    any size for golden
    """
    if type_user == "simple":
        if width > 1280:
            width = 1280
        if height > 720:
            height = 720

    if type_user == "silver":
        if width > 1980:
            width = 1980
        if height > 1080:
            height = 1080

    size = int(width), int(height)
    img = Image.open(image_url[1:])
    temp_img = img.resize(size, Image.ANTIALIAS)
    new_image_url1 = image_url[:image_url.rfind('.')] + "_new1" + image_url[image_url.rfind('.'):]
    new_image_url2 = image_url[:image_url.rfind('.')] + "_new2" + image_url[image_url.rfind('.'):]
    if os.path.exists(new_image_url1[1:]):
        os.remove(new_image_url1[1:])
        new_image_url = new_image_url2
    else:
        if os.path.exists(new_image_url2[1:]):
            os.remove(new_image_url2[1:])
        new_image_url = new_image_url1
    temp_img.save(new_image_url[1:])
    data = {
        "newImage_url": new_image_url,
        "width": width,
        "height": height,
        "type_user": type_user,
    }
    return JsonResponse(data)


"""
This method is called from js file to change contract of image in post
"""


def change_contract_image(request):
    image_url = request.GET.get("image_url", None)
    factor = float(request.GET.get("factor", None))
    image = Image.open(image_url[1:])
    enhancer_object = ImageEnhance.Contrast(image)
    out = enhancer_object.enhance(factor)
    new_image_url1 = image_url[:image_url.rfind('.')] + "_new1" + image_url[image_url.rfind('.'):]
    new_image_url2 = image_url[:image_url.rfind('.')] + "_new2" + image_url[image_url.rfind('.'):]
    if os.path.exists(new_image_url1[1:]):
        os.remove(new_image_url1[1:])
        new_image_url = new_image_url2
    else:
        if os.path.exists(new_image_url2[1:]):
            os.remove(new_image_url2[1:])
        new_image_url = new_image_url1

    out.save(new_image_url[1:])
    data = {
        "newImage_url": new_image_url,
    }
    return JsonResponse(data)


"""
This method is called from js file to rotate of image
"""


def rotate(request):
    image_url = request.GET.get("image_url", None)
    new_image_url = request.GET.get("new_image_url", None)
    clock_wise = request.GET.get("clock_wise", None)
    image = Image.open(new_image_url[1:])
    if clock_wise:
        img = image.rotate(90)
    else:
        img = image.rotate(-90)
    new_image_url1 = image_url[:image_url.rfind('.')] + "_new1" + image_url[image_url.rfind('.'):]
    new_image_url2 = image_url[:image_url.rfind('.')] + "_new2" + image_url[image_url.rfind('.'):]
    if os.path.exists(new_image_url1[1:]):
        os.remove(new_image_url1[1:])
        new_image_url = new_image_url2
    else:
        if os.path.exists(new_image_url2[1:]):
            os.remove(new_image_url2[1:])
        new_image_url = new_image_url1

    img.save(new_image_url[1:])
    data = {
        "newImage_url": new_image_url,
    }
    return JsonResponse(data)


"""
This method is called from js file to transpose of image
"""


def transpose(request):
    new_image_url = request.GET.get("new_image_url", None)
    image_url = request.GET.get("image_url", None)
    image = Image.open(new_image_url[1:])
    transposed_img = image.transpose(Image.FLIP_LEFT_RIGHT)
    new_image_url1 = image_url[:image_url.rfind('.')] + "_new1" + image_url[image_url.rfind('.'):]
    new_image_url2 = image_url[:image_url.rfind('.')] + "_new2" + image_url[image_url.rfind('.'):]
    if os.path.exists(new_image_url1[1:]):
        os.remove(new_image_url1[1:])
        new_image_url = new_image_url2
    else:
        if os.path.exists(new_image_url2[1:]):
            os.remove(new_image_url2[1:])
        new_image_url = new_image_url1
    transposed_img.save(new_image_url[1:])
    data = {
        "newImage_url": new_image_url,
    }
    return JsonResponse(data)


"""
This method is called from js file to add comment to database but this comment isn't approve yet
"""


def user_add_comment(request):
    post_pk = request.GET.get('post_pk', None)
    post = PostModel.objects.get(pk=post_pk)
    post.save()
    comment_text = request.GET.get('comment_text', None)
    comment = CommentPostModel(user=request.user, post=post, text=comment_text)
    comment.save()
    data = {
        "url": "/profile_page/" + str(post.user.pk),
    }
    return JsonResponse(data)


"""
This method is called from js file to to approve comments 
"""


def approve_comment(request):
    comment_pk = request.GET.get('comment_pk', None)
    comment = CommentPostModel.objects.get(pk=comment_pk)
    comment.approve()
    comment.save()
    data = {
        "url": "/profile_page/" + str(request.user.pk),
    }
    return JsonResponse(data)


"""
This method is called from js file to delete comments of post
"""


def delete_comment(request):
    comment_pk = request.GET.get('comment_pk', None)
    comment = CommentPostModel.objects.get(pk=comment_pk)
    comment.delete()
    data = {
        "url": "/profile_page/" + str(request.user.pk),
    }
    return JsonResponse(data)


"""
This method is called from js file to enhance score of image of user post
"""


def add_score_image(request):
    post_pk = request.GET.get("post_pk", None)
    post = PostModel.objects.get(pk=post_pk)
    users_give_score = post.users_give_score.all()
    test = True
    for user in users_give_score.iterator():
        if user.user.id == request.user.id:
            test = False
    if test:
        post.score = post.score + 1
        post.save()
        user_give_score = Users_give_score(user=request.user, post=post)
        user_give_score.save()

        user = UserProfileInfo.objects.filter(user=post.user)[0]
        user.score = user.score + 1
        if 14 > user.score > 12:
            user.typeOfUser = "silver"
        elif user.score > 13:
            user.typeOfUser = "golden"
        user.save()

    data = {
        "new_score": post.score,
        "test": test,
    }
    return JsonResponse(data)
