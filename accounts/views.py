from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .forms import RegistrationForm
from .models import UserProfile

User = get_user_model()

def register(request):
    """ Add a new user """
    # redirect if user is already loggedIn
    if request.user.is_authenticated:
        return redirect(reverse('chat:home'))
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # Process POSTed Form data
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1']
                                    )
            # authenticate and log user in, then redirect to newsFeeds
            login(request, new_user)
            return redirect(reverse('chat:home'))

    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request, username):
    """ view profile of user with username """

    user = User.objects.get(username=username)
    # check if current_user is already following the user
    is_following = request.user.is_following(user)
    return render(request, 'accounts/users_profile.html', {'user': user, 'is_following': is_following})


@login_required
def edit_profile(request):
    """ edit profile of user """
    # A profileInlineFormset helps handle forms of model Relationships
    # The relationship in this case is a OneToOneField
    ProfileInlineFormSet = inlineformset_factory(User, UserProfile, 
                                                 fields=('picture', 'bio', 'phone', 'website', 'address')
                                                 )
    if request.method == "POST":
        # instance kwargs passed in sets the user on the modelForm
        formset = ProfileInlineFormSet(request.POST, request.FILES, instance=request.user)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('accounts:view-profile', args=(request.user.username, )))
    else:
        formset = ProfileInlineFormSet(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'formset': formset})


@login_required
def followers(request):
    """ Return the lists of friends user is  following and not """

    # get users followed by the current_user
    users_followed = request.user.followers.all()
    
    # get_users not followed and exclude current_user from the list
    unfollowed_users = User.objects.exclude(id__in=users_followed).exclude(id=request.user.id)
    return render(request, 'accounts/followers.html', {'users_followed': users_followed, 'unfollowed_users': unfollowed_users})


@login_required
def follow(request, username):
    """ Add user with username to current user's following list """
    
    request.user.followers.add(User.objects.get(username=username))
    return redirect('accounts:followers')


def unfollow(request, username):
    """ Remove username from user's following list """
    request.user.followers.remove(User.objects.get(username=username))
    return redirect('accounts:followers')