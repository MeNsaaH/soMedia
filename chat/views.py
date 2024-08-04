from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm
from .models import Post

@login_required
def home(request):
    """The home news feed page."""
    # Get users whose posts to display on news feed and add user's account
    _users = list(request.user.followers.all())
    _users.append(request.user)

    # Get posts from users' accounts whose posts to display and order by latest
    posts = Post.objects.filter(user__in=_users).order_by('-posted_date')
    comment_form = CommentForm()
    return render(request, 'chat/home.html', {'posts': posts, 'comment_form': comment_form})

@login_required
def add_post(request):
    """Create a new post for the user."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('chat:home')
        else:
            # Handle form errors (e.g., display them on the template)
            return render(request, 'chat/add_post.html', {'form': form})
    else:
        form = PostForm()
    return render(request, 'chat/add_post.html', {'form': form})


@login_required
@require_POST
def add_comment(request, post_id):
    """Add a comment to a post."""
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(Post.objects.get(id=post_id), request.user)
    return redirect(reverse('chat:home'))

@login_required
def delete_post(request, post_id):
    """Delete a post."""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('chat:home')

@login_required
def search_posts(request):
    query = request.GET.get('q', '')
    user_followers = list(request.user.followers.all())
    user_followers.append(request.user)

    if query:
        posts = Post.objects.filter(user__in=user_followers, text__icontains=query).order_by('-posted_date')
    else:
        posts = Post.objects.none()

    results = []
    for post in posts:
        results.append({
            'id': post.id,
            'text': post.text,
            'posted_date': post.posted_date.strftime('%Y-%m-%d %H:%M:%S'),
            'user': f'{post.user.first_name} {post.user.last_name}',
            'picture_url': post.picture.url if post.picture else ''
        })

    return JsonResponse({'results': results})