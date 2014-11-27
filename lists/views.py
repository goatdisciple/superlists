from django.shortcuts import redirect, render

from lists.forms import ItemForm
from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        if request.POST['item_text'] == '':
            error = "You can't have an empty list item"
        else:
            Item.objects.create(text=request.POST['item_text'], list=list_)
            return redirect(list_)
    return render(
        request, 'list.html', {'list': list_, 'error': error})

def new_list(request):
    if request.POST['item_text'] == '':
        return render(
            request, 'home.html', {'error': "You can't have an empty list item"}
        )
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(list_)
