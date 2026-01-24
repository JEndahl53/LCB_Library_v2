# concerts/views/concert_list.py

# from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render
from concerts.models import Concert


# @staff_member_required
def concert_list(request):
    concerts = Concert.objects.select_related('venue').order_by('-date')
    paginator = Paginator(concerts, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "concerts/concert_list.html",
        {
            "concerts": page_obj.object_list,
            "page_obj": page_obj,
        },
    )
