from django.shortcuts import render, get_object_or_404, redirect


from django.http import Http404
from .forms import ProductForm, RawProductForm
from .models import Product


# def product_create_view(request):
#   form = RawProductForm()
#   if request.method == 'POST':
#     form = RawProductForm(data=request.POST)
#     if form.is_valid():
#       print(form.cleaned_data)
#       Product.objects.create(**form.cleaned_data)
#     else:
#       print(form.errors)
#   context = {
#     'form': form
#   }
#   return render(request, 'products/product_create.html', context)


def product_list_view(request):
  queryset = Product.objects.all()
  context = {
    'obj_list': queryset
  }
  return render(request, 'products/product_list.html', context)


def product_create_view(request):
  form = ProductForm()
  if request.method == 'POST':
    form = ProductForm(data=request.POST)
    if form.is_valid():
      form.save()

  context = {
    'form': form
  }
  return render(request, 'products/product_create.html', context)


def product_detail_view(request, id):
  obj = get_object_or_404(Product, id=id)
  context = {
    'obj': obj
  }
  return render(request, 'products/product_detail.html', context)

def product_delete_view(request, id):
  obj = get_object_or_404(Product, id=id)
  # POST request
  if request.method == 'POST':
    obj.delete()
    return redirect('../')
  context = {
    'obj': obj
  }
  return render(request, 'products/product_delete.html', context)
