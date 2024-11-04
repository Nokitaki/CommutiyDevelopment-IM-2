from django.shortcuts import render, redirect, get_object_or_404
from .models import NewsFeed  
from .forms import NewsFeedForm

# Home page showing posts
def home(request):
    form = NewsFeedForm()  # Initialize the form

    if request.method == 'POST':
        form = NewsFeedForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user.username if request.user.is_authenticated else "Anonymous"  # Set to username or "Anonymous"
            new_post.post_type = 'Active'  # Default post type
            new_post.save()
            return redirect('home')

    # Get all active posts ordered by most recent
    newsfeeds = NewsFeed.objects.filter(post_type='Active').order_by('-post_date')
    return render(request, 'newsfeed/home.html', {'form': form, 'newsfeeds': newsfeeds})

# Create a new post
def create_post(request):
    form = NewsFeedForm()  # Initialize the form

    if request.method == 'POST':
        form = NewsFeedForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user.username if request.user.is_authenticated else "Anonymous"  # Set to username or "Anonymous"
            post.save()
            return redirect('home')

    return render(request, 'newsfeed/create_post.html', {'form': form})

# Like a post
def like_post(request, post_id):
    post = get_object_or_404(NewsFeed, id=post_id)
    post.like_count += 1  # Increment the like count
    post.save()
    return redirect('home')

# Update an existing post
def update_post(request, id):
    post = get_object_or_404(NewsFeed, id=id)
    form = NewsFeedForm(instance=post)  # Initialize the form with the existing post

    if request.method == "POST":
        form = NewsFeedForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'newsfeed/update_post.html', {'form': form})

# Delete a post
def delete_post(request, id):
    post = get_object_or_404(NewsFeed, id=id)

    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'newsfeed/confirm_delete.html', {'post': post})
