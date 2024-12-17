from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, EditProfileForm
# from users import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from collections import defaultdict
from .models import SocialMediaLink, LinkClick
from users import models

# Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Login view
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('profile')  # Redirect to a profile page or dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

# Logout view
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


from django.contrib.auth.decorators import login_required
from .forms import CustomUserUpdateForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserUpdateForm
from .models import SocialMediaLink


@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    # Retrieve user's social media links
    links = SocialMediaLink.objects.filter(user=request.user)

    return render(request, 'users/profile.html', {
        'form': form,
        'links': links,  # Pass links to the template
    })




@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Replace with your profile view URL name
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})



from django.shortcuts import get_object_or_404
from .models import CustomUser, LinkClick, SocialMediaLink
from .forms import SocialMediaLinkForm

@login_required
def social_links(request):
    if request.method == 'POST':
        form = SocialMediaLinkForm(request.POST)
        if form.is_valid():
            social_link = form.save(commit=False)
            social_link.user = request.user
            social_link.save()
            return redirect('social_links')
    else:
        form = SocialMediaLinkForm()

    # Fetch all links for the current user
    links = SocialMediaLink.objects.filter(user=request.user)
    return render(request, 'users/social_links.html', {'form': form, 'links': links})

@login_required
def edit_social_link(request, link_id):
    link = get_object_or_404(SocialMediaLink, id=link_id, user=request.user)
    if request.method == 'POST':
        form = SocialMediaLinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            messages.success(request, 'Social media link updated successfully!')
            return redirect('social_links')
    else:
        form = SocialMediaLinkForm(instance=link)

    return render(request, 'users/edit_social_link.html', {'form': form, 'link': link})

@login_required
def delete_social_link(request, link_id):
    link = get_object_or_404(SocialMediaLink, id=link_id, user=request.user)
    link.delete()
    messages.success(request, 'Social media link deleted successfully!')
    return redirect('social_links')

from django.shortcuts import get_object_or_404, render
from .models import CustomUser, SocialMediaLink

from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import SocialMediaLink, LinkClick

@login_required
def public_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    social_links = user.social_links.all()

    # Fetch click trends for each link grouped by date
    most_clicked_links = []
    for link in social_links:
        daily_clicks = (
            LinkClick.objects.filter(link=link)
            .annotate(date=TruncDate('clicked_at'))
            .values('date')
            .annotate(click_count=Count('id'))
            .order_by('date')
        )
        link.daily_clicks = list(daily_clicks)  # Attach daily trends to each link
        most_clicked_links.append(link)

    return render(request, 'users/public_profile.html', {
        'user': user,
        'social_links': social_links,
        'most_clicked_links': most_clicked_links,
    })



from django.db.models import Q  # Import Q for complex queries
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render

@login_required
def search_profiles(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Search for users by username or bio, excluding the current user
        results = CustomUser.objects.filter(
            Q(username__icontains=query) | Q(bio__icontains=query)
        ).exclude(id=request.user.id)

    # Paginate the results
    paginator = Paginator(results, 10)  # 10 results per page
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # Deliver the first page
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Deliver the last page

    # Pass the query, paginated results, and logged-in user's following list
    return render(request, 'users/search_profiles.html', {
        'query': query,
        'page_obj': page_obj,
        'following': request.user.following.all(),  # Fetch all users the current user follows
    })


from collections import defaultdict
from django.db.models import Count

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from collections import defaultdict
from .models import SocialMediaLink, LinkClick

@login_required
def dashboard(request):
    links = request.user.social_links.all()
    most_clicked_links = links.order_by('-click_count')[:5]
    total_clicks = sum(link.click_count for link in links)

    # Prepare daily click data for line graph
    daily_clicks = defaultdict(list)
    for link in links:
        clicks = LinkClick.objects.filter(link=link).values('clicked_at').annotate(count=Count('id')).order_by('clicked_at')
        for click in clicks:
            daily_clicks[link.id].append((click['clicked_at'], click['count']))

    return render(request, 'users/dashboard.html', {
        'most_clicked_links': most_clicked_links,
        'total_clicks': total_clicks,
        'daily_clicks': daily_clicks
    })



from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Follow

from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Follow

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Follow

@login_required
def view_followers(request, username):
    # Fetch the profile user
    profile_user = get_object_or_404(CustomUser, username=username)

    # Allow only the user to view their followers
    if request.user == profile_user:
        # Use `select_related` to optimize the queryset and avoid fetching issues
        followers = Follow.objects.filter(followed=profile_user).select_related('follower')
    else:
        # Hide the list of followers if it's not their profile
        followers = None

    # Pass the followers and profile_user to the template
    return render(request, 'users/followers.html', {'profile_user': profile_user, 'followers': followers})



@login_required
def view_following(request, username):
    # Fetch the profile user
    profile_user = get_object_or_404(CustomUser, username=username)

    # Allow only the user to view their following list
    if request.user == profile_user:
        # Use `select_related` to optimize the queryset and fetch related data
        following = Follow.objects.filter(follower=profile_user).select_related('followed')
    else:
        # Hide the list of following users if it's not their profile
        following = None

    # Pass the following and profile_user to the template
    return render(request, 'users/following.html', {'profile_user': profile_user, 'following': following})






@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(CustomUser, id=user_id)
    if followed_user != request.user:
        Follow.objects.get_or_create(follower=request.user, followed=followed_user)
    return redirect('public_profile', username=followed_user.username)

@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(CustomUser, id=user_id)
    Follow.objects.filter(follower=request.user, followed=followed_user).delete()
    return redirect('home')

@login_required
def notifications(request):
    user_notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'users/notifications.html', {'notifications': user_notifications})


@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/profile.html', {'user': user})




from django.http import HttpResponseRedirect
from django.utils import timezone

def track_click(request, link_id):
    link = get_object_or_404(SocialMediaLink, id=link_id)
    link.click_count += 1
    link.save()

    # Log the click for daily analytics
    LinkClick.objects.create(link=link, clicked_at=timezone.now())

    return HttpResponseRedirect(link.url)

from django.shortcuts import redirect, get_object_or_404
from .models import SocialMediaLink

from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from .models import SocialMediaLink, LinkClick
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import SocialMediaLink, LinkClick

@login_required
def track_social_link(request, link_id):
    """
    Tracks clicks on social media links, excluding clicks by the owner.
    Logs daily analytics for non-owner clicks.
    """
    link = get_object_or_404(SocialMediaLink, id=link_id)
    
    # Only increment click count if the user is not the link owner
    if request.user != link.user:
        link.increment_click_count()  # Custom method to increment count
        
        # Log the click for daily analytics
        LinkClick.objects.create(link=link, clicked_at=timezone.now())

    # Redirect the user to the link URL
    return HttpResponseRedirect(link.url)


    # Redirect to the actual link



# users/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'users/home.html')
