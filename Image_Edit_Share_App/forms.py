from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Image_Edit_Share_App.models import UserProfileInfo, PostModel
from django import forms


class UserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True, help_text="enter your password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True, help_text="enter your password again")
    first_name = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'


class UserProfileInfoForm(forms.ModelForm):
    # profile_pic = forms.ImageField(widget=forms.TextInput(attrs={'class' :'btn btn-primary' 'btn-sm' 'float-left'}))
    # bio = forms.TextInput(widget=forms.TextInput(attrs={'class' :'btn btn-primary' 'btn-sm' 'float-left'}))
    class Meta:
        model = UserProfileInfo
        fields = ('profile_pic', 'bio',)


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ("image",)
