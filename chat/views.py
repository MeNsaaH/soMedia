from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm
from .models import Post


@login_required
def home(request):
	""" The home news feed page """

	# Get users whose posts to display on news feed and add users account
	_users = list(request.user.followers.all())
	_users.append(request.user)

	# Get posts from users accounts whose posts to display and order by latest
	posts = Post.objects.filter(user__in=_users).order_by('-posted_date')
	comment_form = CommentForm()
	return render(request, 'chat/home.html', {'posts': posts, 'comment_form': comment_form})


@login_required
def add_post(request):
	""" create a new posts to user """
	# handle only POSTed Data
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		# validate form based on form definition
		if form.is_valid():
			post = form.save(commit=False)
			# add the post user to the existing form
			# this method can be declared in the postForm easily by overiding the save() method
			# and adding user before saving.
			# See implementation of CommentForm
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
		# pass the post id to the comment save() method which was overriden
		# in the CommentForm implementation
		comment = form.save(Post.objects.get(id=post_id), request.user)
	return redirect(reverse('chat:home'))
