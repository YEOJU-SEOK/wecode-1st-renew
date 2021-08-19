import json

from django.views import View
from django.http import JsonResponse

from menu.models import Category, SubCategory

class CategoryView(View):
    def get(self, request):

        categories = Category.objects.prefetch_related('subcategory_set').all()

        categories = [{ 
            'categoryId'   : category.id,
            'category'     : category.name,
            'subCategories': [
                sub_category.name
                for sub_category in category.subcategory_set.all()]
            } for category in categories]
        
        return JsonResponse({"categories" : categories}, status=200)
        
       
         
         

  
    