from typing import Any
from blog.models import Category
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self,*args:Any,**options:Any):
        Category.objects.all().delete()
        name=['Sports','Technology','Science','Art','Food']

        for category_name in name:
            Category.objects.create(name=category_name)

        self.stdout.write(self.style.SUCCESS('Completed Inserting Data!'))