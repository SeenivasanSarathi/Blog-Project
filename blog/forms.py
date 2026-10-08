from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import post,Category

class PostForm(forms.Form):
    name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(max_length=200,required=True)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=100,required=True)
    confirm_password = forms.CharField(max_length=100,required=True)

    class Meta:
        model = User
        fields = ['username','email','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password!=confirm_password:
            raise forms.ValidationError("Password Does not match!")
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,required=True)
    password = forms.CharField(max_length=100,required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username = username,password = password)
            if user is None:
                raise forms.ValidationError('Username and Password is Incorrect!')
            
class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100,required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Entered Email Id Not Found!')
    
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(max_length = 100,required=True)
    confirm_password = forms.CharField(max_length = 100,required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password!=confirm_password:
            raise forms.ValidationError("Password doesn't match")
        
class NewPost(forms.ModelForm):
    title = forms.CharField(max_length=100,required=True)
    content = forms.CharField(required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),required=True)
    img_url = forms.ImageField(required = False)

    class Meta:
        model = post
        fields = ['title','content','category','img_url']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and len(title) < 5:
            raise forms.ValidationError('Title should not be less than 5 characters')
        
        if content and len(content) < 10:
            raise forms.ValidationError('Content should not be less than 10 characters')
        
        def save(self,commit=...):
            post = super().save(commit)

            if self.cleaned_data['img_url']:
                post.img_url = self.cleaned_data['img_url']
            else:
                post.img_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6eoP22fr1gee9ZOkWtUS0frFs_ZYwV0SCwrGuI14ebw&s=10"

            if commit==True:
                post.save()

            