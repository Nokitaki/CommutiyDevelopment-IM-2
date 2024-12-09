# resourcehub/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ResourceHub, Category
from .forms import ResourceForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
import os
import bleach
import logging
logger = logging.getLogger(__name__)


@csrf_exempt
def upload_image(request):
    try:
        if request.method == 'POST':
            # TinyMCE typically sends the file under 'file'
            image = request.FILES.get('file')
            
            if image:
                # Generate a unique filename to prevent overwriting
                from django.utils.crypto import get_random_string
                import os
                
                file_extension = os.path.splitext(image.name)[1]
                file_name = f"{get_random_string(10)}{file_extension}"
                upload_path = os.path.join('uploads', file_name)
                
                # Ensure the upload directory exists
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                
                # Save the file
                with open(upload_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                
                # Return the URL in the format TinyMCE expects
                return JsonResponse({
                    'location': f'/uploads/{file_name}'
                })
        
        return JsonResponse({'error': 'Upload failed'}, status=400)
    
    except Exception as e:
        logger.error(f"Image upload error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def resource_list(request):
    resources = ResourceHub.objects.all().order_by('-upload_date')
    categories = Category.objects.all()
    form = ResourceForm()
    
    return render(request, 'resourcehub/home.html', {
        'resources': resources,
        'categories': categories,
        'form': form
    })

@login_required
def create_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.created_by = request.user
            resource.save()
            messages.success(request, 'Resource created successfully!')
            return redirect('resource_home')
        else:
            messages.error(request, 'Error creating resource. Please check your input.')
            print(form.errors)  # This will help debug form errors
    return redirect('resource_home')

@login_required
def like_resource(request, resource_id):
    if request.method == 'POST':
        resource = get_object_or_404(ResourceHub, resource_id=resource_id)
        resource.heart_count += 1
        resource.save()
        return JsonResponse({
            'status': 'success',
            'heart_count': resource.heart_count
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def update_resource(request, resource_id):
    resource = get_object_or_404(ResourceHub, resource_id=resource_id, created_by=request.user)
    
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource updated successfully!')
            return redirect('resource_home')
        else:
            messages.error(request, 'Error updating resource. Please check your input.')
    
    return redirect('resource_home')

@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(ResourceHub, resource_id=resource_id, created_by=request.user)
    
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted successfully!')
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_resource_details(request, resource_id):
    resource = get_object_or_404(ResourceHub, resource_id=resource_id)
    
    data = {
        'title': resource.resource_title,
        'description': mark_safe(resource.resource_description),
        'author_name': f"{resource.created_by.firstname} {resource.created_by.lastname}",
        'upload_date': resource.upload_date.strftime('%B %d, %Y'),
        'download_count': resource.download_count,  # Changed from heart_count
        'image_url': resource.image.url if resource.image else None,
        'category': resource.category.name if resource.category else None,
    }
    
    return JsonResponse(data)
    
@login_required
def download_resource(request, resource_id):
    try:
        resource = get_object_or_404(ResourceHub, resource_id=resource_id)
        resource.download_count += 1  # Changed from heart_count to download_count
        resource.save()
        return JsonResponse({
            'status': 'success',
            'download_count': resource.download_count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


