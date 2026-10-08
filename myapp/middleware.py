from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        if request.user.is_authenticated:
            path_to_restricts = [reverse('register'),reverse('login')]

            if request.path in path_to_restricts:
                return redirect('dashboard')
            
        response = self.get_response(request)
        return response
    

class RestrictUnAuthenticatedUserMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        if not request.user.is_authenticated:
            path_to_restricts=[reverse('dashboard')]

            if request.path in path_to_restricts:
                return redirect('login')
        response = self.get_response(request)
        return response