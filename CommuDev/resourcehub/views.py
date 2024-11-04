from django.shortcuts import render, redirect, get_object_or_404
from .models import ResourceHub
from .forms import ResourceForm
from django.http import JsonResponse

def resource_list(request):
    resources = ResourceHub.objects.all().order_by('-upload_date')  # Get all resources ordered by upload date
    return render(request, 'resourcehub/home.html', {'resources': resources})

def create_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)  # Don't save to the database yet
            resource.created_by = "Anonymous"   # Set created_by to "Anonymous"
            resource.save()                      # Now save it to the database
            return redirect('resource_home')
    else:
        form = ResourceForm()

    resources = ResourceHub.objects.all()
    return render(request, 'resourcehub/create_resource.html', {'form': form, 'resources': resources})

def like_resource(request, resource_id):
    if request.method == 'POST':
        # Changed id to resource_id to match your model's primary key field
        resource = get_object_or_404(ResourceHub, resource_id=resource_id)
        resource.heart_count += 1
        resource.save()
    return redirect('resource_home')

def update_resource(request, resource_id):
    resource = get_object_or_404(ResourceHub, resource_id=resource_id)
    if request.method == "POST":
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_home')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resourcehub/update_resource.html', {'form': form})

def delete_resource(request, resource_id):
    # Check if the request method is POST
    if request.method == 'POST':
        resource = get_object_or_404(ResourceHub, resource_id=resource_id)  # Get the resource
        resource.delete()  # Delete the resource
        return redirect('resource_home')  # Redirect to the resource list page
