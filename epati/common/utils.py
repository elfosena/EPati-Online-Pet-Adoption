from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from adopt.models import Pet, Kind

def pagination_helper(list, page_number, items_per_page):
    p = Paginator(list, items_per_page)
    try:
        page = p.page(page_number)
    except EmptyPage:
        page = p.page(1)

    return page

def search_helper(search_str, pet_list, kind):
    search_results = Pet.objects.filter(Q(name__icontains=search_str) |        
                Q(description__icontains=search_str) | 
                Q(kind__name__icontains=search_str) |
                Q(breed__icontains=search_str) | 
                Q(age__icontains=search_str) | 
                Q(description__icontains=search_str))
                
    pet_list = list(search_results.values())
    return pet_list