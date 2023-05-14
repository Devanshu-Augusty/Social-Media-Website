from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

# Create your views here.

@login_required(login_url = 'login')
def index(request):
    posts = Post.objects.all()
    # user_profile = Profile.objects.get(user = posts.username)
    # user_profile = Profile.objects.all()
    

    context = {
        'posts': posts,
        # 'user_profile': user_profile
    }

    return render(request, 'index.html', context)

@login_required(login_url = 'login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(username = user, image = image, caption = caption)
        new_post.save()
        return redirect('home')

    else:
        return redirect('home')

@login_required(login_url='login')
def settings(request):
    loggedIn_user = Profile.objects.get(user = request.user) # request.user is the user that is logged in to make sure that he opens his account settings only
    context = {'loggedIn_user':loggedIn_user}

    if request.method == 'POST':
        if request.FILES.get('image') == None: # means user did not upload any image then we want to keep the same image
            bio = request.POST.get('bio')
            location = request.POST.get('location')

            loggedIn_user.bio = bio
            loggedIn_user.location = location
            loggedIn_user.save()
        else:
            image = request.FILES.get('image')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
    
            loggedIn_user.profile_img = image
            loggedIn_user.bio = bio
            loggedIn_user.location = location
            loggedIn_user.save()
        
        return redirect('settings')

    return render(request, 'settings.html', context)

# def settings(request):
    user_profile = Profile.objects.get(user = request.user) # request.user is the user that is logged in to make sure that he opens his account settings only
    context = {'user_profile': user_profile}

    if request.method == 'POST':
        
        if request.FILES.get('image') == None: # bohot confuse hua be sabka same same hi rakhunga agli barr
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')


    # return render(request, "settings.html", context)

@login_required(login_url = 'login')
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(username = pk) #filter() method returns a QuerySet object that can contain multiple objects, whereas the get() method returns a single object, or raises an exception if none or multiple objects are found.
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowerCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowerCount.objects.filter(user = pk))
    user_following = len(FollowerCount.objects.filter(follower=pk))

    context = {
        'user_profile': user_profile,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')

        if FollowerCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowerCount.objects.get(follower=follower, user = user)
            delete_follower.delete()
            return redirect('profile/'+user)
        else:
            new_follower = FollowerCount.objects.create(follower = follower, user = user)
            new_follower.save()
            return redirect('profile/'+user)
    else:
        return redirect('home')

@login_required(login_url = 'login')
def likes(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id = post_id)

    # .filter(post_id=post_id, username=username): This applies a filter to the query, specifying that we want to find records where the post_id field matches the given post_id value and the username field matches the given username value.
    #.first(): This retrieves the first record that matches the filter criteria, or returns None if no matching records are found. Since we are using first() instead of get(), we expect at most one record to match the filter criteria. If there are multiple records that match the filter criteria, first() will return only the first one.
    # The resulting like_filter variable will contain either the first matching record from the LikePost model or None if no matching record is found. This allows you to check if a user has already liked a post, and take appropriate action based on the result.
    like_filter = Likes.objects.filter(post_id = post_id, user = username).first()

    if like_filter == None: #user haven't liked the post
        new_like = Likes.objects.create(post_id = post_id, user = username) # username -> the one who is liking the post
        new_like.save()
        post.likes += 1
        post.save()
        return redirect('home')
    else:
        like_filter.delete()
        post.likes -= 1
        post.save()    
        return redirect('home')

@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        value = request.POST.get('search')
        user = Profile.objects.filter(user__username__icontains = value) 
        # The user__username lookup syntax in Django is used to perform a lookup on a related model field. In this case, it's assuming that there is a one-to-one 
        # or foreign key relationship between the Profile model and a User model, where User has a field called username.
        # If your Profile model has a field named user that is a foreign key to the User model, then you can use user__username
            
        return render(request, 'search.html', {'profile_list' : user})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_pass = request.POST.get('c_pass')

        if password != c_pass:
            messages.info(request, 'passwords not matching')
            return redirect('signup')
        elif User.objects.filter(username = username).exists(): # return true or false
            messages.info(request, 'Username already exists')
            return redirect('signup')
        elif User.objects.filter(email = email).exists():
            messages.info(request, 'E-mail already exists')
            return redirect('signup')
        else:
            # creating user 
            create_user = User.objects.create_user(username=username, email=email, password=password)
            create_user.save()

            # logging the user in the wesite directly
            user_login = auth.authenticate(username = username, password = password) # getting user info from the database
            auth.login(request, user_login)

            # save te user data in Profile Model
            user_model = User.objects.get(username = username) # have to do this cause can't just pass a random name in Profile model
            profile_model = Profile.objects.create(user = user_model)
            profile_model.save()
            return redirect('settings')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password) # getting user info from the database

        if user is None:
            messages.info(request, 'Wrong username or password')
            return redirect('login')
        else:
            auth.login(request, user)
            return redirect('home')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
