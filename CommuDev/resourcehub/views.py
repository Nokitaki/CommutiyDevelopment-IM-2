# resourcehub/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ResourceHub
from .forms import ResourceForm

@login_required
def resource_list(request):
    resources = ResourceHub.objects.all().order_by('-upload_date')
    return render(request, 'resourcehub/home.html', {'resources': resources})

@login_required
def create_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.created_by = request.user
            resource.save()
            return redirect('resource_home')
    else:
        form = ResourceForm()
    return render(request, 'resourcehub/create_resource.html', {'form': form})

@login_required
def like_resource(request, resource_id):
    if request.method == 'POST':
        resource = get_object_or_404(ResourceHub, resource_id=resource_id)
        resource.heart_count += 1
        resource.save()
    return redirect('resource_home')

@login_required
def update_resource(request, resource_id):
    resource = get_object_or_404(ResourceHub, resource_id=resource_id)
    if request.user != resource.created_by:
        return redirect('resource_home')
    
    if request.method == "POST":
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_home')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resourcehub/update_resource.html', {'form': form})

@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(ResourceHub, resource_id=resource_id)
    if request.user != resource.created_by:
        return redirect('resource_home')
        
    if request.method == 'POST':
        resource.delete()
        return redirect('resource_home')
    return render(request, 'resourcehub/delete_form.html', {'resource': resource})