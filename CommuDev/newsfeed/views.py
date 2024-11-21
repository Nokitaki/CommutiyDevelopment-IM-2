from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NewsFeed  
from .forms import NewsFeedForm

@login_required
def home(request):
    form = NewsFeedForm()
    if request.method == 'POST':
        form = NewsFeedForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user
            new_post.post_type = 'Active'
            new_post.save()
            return redirect('home')
    newsfeeds = NewsFeed.objects.filter(post_type='Active').order_by('-post_date')
    return render(request, 'newsfeed/home.html', {'form': form, 'newsfeeds': newsfeeds})

@login_required
def create_post(request):
    form = NewsFeedForm()
    if request.method == 'POST':
        form = NewsFeedForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('home')
    return render(request, 'newsfeed/create_post.html', {'form': form})

@login_required
def like_post(request, feed_id):
    post = get_object_or_404(NewsFeed, feed_id=feed_id)
    post.like_count += 1
    post.save()
    return redirect('home')

@login_required
def update_post(request, feed_id):
    post = get_object_or_404(NewsFeed, feed_id=feed_id)
    if request.user != post.created_by:
        return redirect('home')
    form = NewsFeedForm(instance=post)
    if request.method == "POST":
        form = NewsFeedForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'newsfeed/update_post.html', {'form': form})

@login_required
def delete_post(request, feed_id):
    post = get_object_or_404(NewsFeed, feed_id=feed_id)
    if request.user != post.created_by:
        return redirect('home')
    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, 'newsfeed/confirm_delete.html', {'post': post})