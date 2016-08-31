from django.shortcuts import render, get_object_or_404
from .models import NonMediaItem

# Create your views here.
def detail(request, item_id):
    i = get_object_or_404(NonMediaItem, pk=item_id)
    return render(request, 'ecommerce/detail.html', {'item': i, 'id': item_id})
