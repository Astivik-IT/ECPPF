from django.shortcuts import render, redirect

from . import forms
from . import models

def proveedor(request):
    if request.method == 'POST':
        form = forms.mantenerProveedor(request.POST)
        if form.is_valid():
            newprov = models.proveedor(nit = form.cleaned_data['nit'])
            newprov = models.proveedor(nombre = form.cleaned_data['nombre'])
            newprov = models.proveedor(email = form.cleaned_data['email'])
            newdoc.save(form)
            
            #forms.Termine(request.POST, request.FILES)
            #return render(request, 'proveedores/mantenerProveedor.html', {'form': form})
            return redirect("mensaje")
    else:
        form = forms.mantenerProveedor()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'proveedores/mantenerProveedor.html', {'form': form})
