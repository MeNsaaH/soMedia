from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import PostForm, CommentForm
from .models import Post

@login_required
def home(request):
	_users = list(request.user.followers.all())
	_users.append(request.user)
	
	posts = Post.objects.filter(user__in=_users).order_by('-posted_date')
	comment_form = CommentForm()
	return render(request, 'chat/home.html', {'posts': posts, 'comment_form': comment_form})


@login_required
def add_post(request):
	""" create a new posts to user """

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('chat:home')
	else:
		form = PostForm()
	return render(request, 'chat/add_post.html', {'form': form})


@login_required
@require_POST
def add_comment(request, post_id):
	""" Add a comment to a post """

	form = CommentForm(request.POST)
	if form.is_valid():
		comment = form.save(Post.objects.get(id=post_id), request.user)
	return redirect(reverse('chat:home'))
