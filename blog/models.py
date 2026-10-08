from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    
class post(models.Model):
    title = models.CharField( max_length=50)
    content = models.TextField()
    img_url = models.ImageField(upload_to = "post/images",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    @property 
    def formatted_url(self):
        url = self.img_url if self.img_url.__str__().startswith(('http://','https://')) else self.img_url.url
        return url

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title


class About_Us(models.Model):
    content = models.TextField()    

