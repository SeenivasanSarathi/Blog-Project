from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import post,About_Us,Category
from django.http import Http404

from django.core.paginator import Paginator
from .forms import LoginForm, NewPost, PostForm,RegisterForm,ForgetPasswordForm, ResetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
# Create your views here.

def index(request):
    # post_details = {
    #     'item' :[
    #         {'id':1,'post_title':'Post1','post_des':'Post description'},
    #         {'id':2,'post_title':'Post2','post_des':'Post description'},
    #         {'id':3,'post_title':'Post3','post_des':'Post description'},
    #         {'id':4,'post_title':'Post4','post_des':'Post description'},
    #         {'id':5,'post_title':'Post5','post_des':'Post description'},
    #     ]
    # }

    try:
        post_details = post.objects.all() 
        paginator = Paginator(post_details,5)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

    except Exception as e:
        return Http404("Page Does not Exist!")
    return render(request,'blog/index.html',{'page_obj':page_obj})

def detail(request,slug):
    post_details = post.objects.get(slug=slug)
    related_posts = post.objects.filter(category = post_details.category).exclude(pk=post_details.id)
    return render(request,'blog/detail.html',{'post_details':post_details,'related_posts':related_posts})

def olr_url_redirect(request):
    return redirect(reverse("new"))

def new_url_view(request):
    return HttpResponse("This is the new URL page")

def contact(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if form.is_valid():
            success_message = "Your Email has been sent !"
            return render(request,'blog/contact.html',{'success_message':success_message})
        return render(request,'blog/contact.html',{'form':form,'name':name,'email':email,'message':message})

    return render(request,'blog/contact.html')    

def about(request):
    about_content = About_Us.objects.first()
    if about_content is None or not about_content.content:
        about_content = "No About Content Exist!"
    else:
        about_content = about_content.content
    return render(request,'blog/about.html',{'about_content':about_content})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
            messages.success(request,'Registration Successfull.You can Login!')
            
    return render(request,'blog/register.html',{'form':form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username and password:
                user = authenticate(username = username,password = password)
                if user is not None:
                    auth_login(request,user)
                    return redirect('dashboard')
    return render(request,'blog/login.html',{'form':form})

def dashboard(request):
    post_details = post.objects.filter(user=request.user)
    paginator = Paginator(post_details,5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request,'blog/dashboard.html',{'page_obj':page_obj})

def logout(request):
    auth_logout(request)
    return redirect('index')

def forget_password(request):
    form = ForgetPasswordForm()
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = " Request For Reset Password "
            message = render_to_string('blog/reset_password_email.html',{'domain':domain,'uid':uid,'token':token})
            send_mail(subject,message,'noreply@gmail.com',[email])
            messages.success(request,'Email has been sent!')

    return render(request,'blog/forget_password.html',{'form':form})

def reset_password(request,uidb64,token):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user = None
            
            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Updated you can login')
                return redirect('login')
            else:
                messages.error(request,'Link expired!')
    return render(request,'blog/reset_password.html',{'form':form})

def newpost(request):
    categories = Category.objects.all()
    form = NewPost()
    if request.method == 'POST':
        form = NewPost(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('dashboard')
    return render(request,'blog/newpost.html',{'form':form,'categories':categories})

def edit_post(request,post_id):
    categories = Category.objects.all()
    Post = get_object_or_404(post,id=post_id)
    form = NewPost()
    if request.method == 'POST':
        form = NewPost(request.POST,request.FILES,instance=Post)
        if form.is_valid():
            form.save()
            messages.success(request,"Post Updated Successfully!")
            return redirect('dashboard')
    return render(request,'blog/edit_post.html',{'categories':categories,'post':Post})

def delete_post(request,post_id):
    Post = get_object_or_404(post,id=post_id)
    Post.delete()
    return redirect('dashboard')


