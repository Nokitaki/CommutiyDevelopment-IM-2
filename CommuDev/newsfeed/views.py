from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NewsFeed  
from .forms import NewsFeedForm
from django.views.decorators.http import require_POST

@login_required
def home(request):
    form = NewsFeedForm()
    if request.method == 'POST':
        form = NewsFeedForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user
            new_post.save()
            return redirect('home')
    newsfeeds = NewsFeed.objects.filter(post_type='Active').order_by('-post_date')
    return render(request, 'newsfeed/home.html', {'form': form, 'newsfeeds': newsfeeds})


@login_required
def like_post(request, feed_id):
    post = get_object_or_404(NewsFeed, feed_id=feed_id)
    post.like_count += 1
    post.save()
    return redirect('home')

@login_required
@require_POST
def update_post(request, feed_id):
    post = get_object_or_404(NewsFeed, feed_id=feed_id, created_by=request.user)
    try:
        data = json.loads(request.body)
        post.post_description = data.get('post_description')
        post.save()
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_POST
def delete_post(request, feed_id):
    post = get_object_or_404(NewsFeed, feed_id=feed_id, created_by=request.user)
    try:
        post.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)