from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
import mimetypes
from django.http import FileResponse,HttpResponseBadRequest

from carro.carro import Carro
from usuario.decorator import role_required
# Create your views here.
from .form import ProductForm,ProductUpdateForm , ProductAttachmentInlineFormSet
from .models import Product, ProductImage, ClasificacionPadre,ClasificacionHija


@role_required(['Proveedor'])
def product_create_view(request):
    context={}
    form = ProductUpdateForm(request.POST or None,  request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect(obj.get_manage_url())
        else:
            form.add_error(None,"Your  must be looged in to create product")
    context['form'] = form
    return render(request, 'products/create.html',context)

def product_list_view(request):
    object_list = Product.objects.all()
    classifications = ClasificacionPadre.objects.all()
    carro = Carro(request)

    # Handle search query
    search_query = request.GET.get('search')
    if search_query:
        object_list = object_list.filter(keywords__icontains=search_query)

    # Handle classification filter
    classification_id = request.GET.get('classification_id')
    if classification_id:
        object_list = object_list.filter(clasificacion__id=classification_id)

    classification_id_padre = request.GET.get('classification_id_padre')
    if classification_id_padre:
        object_list = object_list.filter(clasificaciones_padre__id=classification_id_padre)





    # Paginar los productos
    page_size = 20  # Número de solicitudes por página
    paginator = Paginator(object_list, page_size)
    page_number = request.GET.get('page', 1)

    try:
        page_solicitudes = paginator.page(page_number)
    except PageNotAnInteger:
        page_solicitudes = paginator.page(1)
    except EmptyPage:
        page_solicitudes = paginator.page(paginator.num_pages)


    context = {
        'object_list': page_solicitudes,
        'carro': carro,
        'classifications': classifications,
    }
    return render(request,"products/list.html",context)




@role_required(['Proveedor'])
def product_manage_detail_view(request,handle=None):
    obj = get_object_or_404(Product,handle=handle)
    attachments = ProductImage.objects.filter(product=obj)
    is_manager = False

    if request.user.is_authenticated:
        is_manager = obj.user == request.user
    context = {"object": obj}

    if not is_manager:
        return HttpResponseBadRequest("No eres proveedor de este producto")
    form = ProductUpdateForm(request.POST or None,  request.FILES or None, instance=obj)
    formset = ProductAttachmentInlineFormSet(request.POST or None,request.FILES or None,queryset=attachments)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()  # Guarda las relaciones ManyToMany

        formset.save(commit=False)
        for _form in formset:

            is_delete = _form.cleaned_data.get("DELETE")

            try:
                attachments_obj = _form.save(commit=False)
            except:
                attachments_obj = None
            if is_delete:
                if attachments_obj is not None:
                   if attachments_obj.pk:
                       attachments_obj.delete()
            else:
                if attachments_obj is not None:
                    attachments_obj.product = instance
                    attachments_obj.save()


        return redirect(obj.get_manage_url())
    context['form'] = form
    context['formset'] = formset
    return render(request, 'products/manager.html', context)

def product_detail_view(request,handle=None):
    obj = get_object_or_404(Product,handle=handle)
    attachments = ProductImage.objects.filter(product=obj)
    # attachments = obj.productattachment_set.all()
    is_owner = False

    if request.user.is_authenticated:
        is_owner = True # verify ownership
    context = {"object": obj, "is_owner": is_owner,"attachments":attachments}

    return render(request, 'products/detail.html', context)


def product_attachment_download_view(request,handle=None,pk=None):
    attachment = get_object_or_404(ProductImage,product__handle=handle,pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True # check ownership
    if can_download is False:
        return HttpResponseBadRequest
    file=attachment.file.open(mode='rb') # cdn -> 53 object storage
    filename = attachment.file.name
    content_type, _encoding = mimetypes.guess_type(filename)
    response = FileResponse(file)
    response['Conten-Type'] = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response


def mis_productos_table(request):
    return render(request, 'products/mis_productos_table.html')
