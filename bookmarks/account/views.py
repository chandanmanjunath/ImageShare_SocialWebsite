#For generating a HttpResponse
from django.http import HttpResponse
#render final data required to display in html template
from django.shortcuts import render
#Use authenticate and login functionalities provided by django.contrib.auth
from django.contrib.auth import authenticate, login
#Import the login form ,previously created by us
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
#importing get_object_or_404 from shortcuts
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Import the profile model created
from .models import Profile

#Import the messages from django.contrib
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact
from actions.models import Action

from actions.utils import create_action

def user_login(request):
    #if the login form is submitted
    if request.method == 'POST':
        #Load the form instance with the request object data
        form = LoginForm(request.POST)
        #Check if form is valid
        if form.is_valid():
            #Place the cleaned form data into cd dictionay
            cd = form.cleaned_data
            #authnticate the data and return user object
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            #if the user is authenticated one ,it should not be None
            if user is not None:
                #Check if user is active or not
                if user.is_active:
                    #allow user to login to application
                    login(request, user)
                    #Disply the success message usong HttpResponse
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    #If the user is inactive display failurei.e.deactivate message
                    return HttpResponse('Disabled account')
        else:
            #if the form data is invalid display the message as invalid
            return HttpResponse('Invalid login')
    else:
            #If its a initial request load the loginForm
            form = LoginForm()
    #return the respective html template and  dictionary containing form keyword
    return render(request, 'account/login.html', {'form': form})

#Login required is the decorator given by django authentication framework
#to identify authentic user if so this will call the below view
@login_required
def dashboard(request):
        # Display all actions by default
        actions = Action.objects.exclude(user=request.user)
        #get the id values of user following
        following_ids = request.user.following.values_list('id',
                                                     flat=True)
        if following_ids:
            # If user is following others, retrieve only their actions
            #actions = actions.filter(user_id__in=following_ids)
            #related foreign key references can be provided by selecting the user field and profile field
            #select_related is used for ForeignKey or onetoone relation
            actions = actions.filter(user_id__in=following_ids)\
                                    .select_related('user', 'user__profile')\
                                    .prefetch_related('target')
        #get the latest 10 actions
        actions = actions[:10]
        return render(request,'account/dashboard.html',{'section': 'dashboard','actions': actions})



def register(request):
        #identify post method
        if request.method == 'POST':
            #get the instance of submitted form
            user_form = UserRegistrationForm(request.POST)
            #if form is valid
            if user_form.is_valid():
                    # Create a new user object but avoid saving it yet
                    new_user = user_form.save(commit=False)
                    # Set the chosen password,set_password method encryptes the password
                    new_user.set_password(user_form.cleaned_data['password'])
                    # Save the User object after the encrypted password
                    new_user.save()
                    # Create the user profile
                    #Create a new profile when user is registered.
                    profile = Profile.objects.create(user=new_user)
                    #recording the actions created
                    create_action(new_user, 'has created an account')
                    return render(request,
                                'account/register_done.html',
                                {'new_user': new_user})
        else:
                user_form = UserRegistrationForm()
                return render(request,
                        'account/register.html',
                        {'user_form': user_form})


#decorator used to authenticate the user
@login_required
def edit(request):
        if request.method == 'POST':
                #create a user_form object
                #Use request.user instance
                #data use request.Post data
                user_form = UserEditForm(instance=request.user,
                                        data=request.POST)
                #create a profile_form object
                #use request.user.profile instance
                #The user object is referenced from  model class
                #The profile object is referenced from register method above
                profile_form = ProfileEditForm(instance=request.user.profile,
                                                data=request.POST,
                                               files=request.FILES)
                #Check if both user_form and profile_form is valid
                if user_form.is_valid() and profile_form.is_valid():
                        #save respective details to database
                        user_form.save()
                        profile_form.save()
                        messages.success(request, 'Profile updated successfully')
                else :
                        #Use the messages framework to display error  if form and profile are not valid
                        messages.error(request, 'Error updating your profile')
        #else load the original form instance
        else:
                user_form = UserEditForm(instance=request.user)
                profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                    'account/edit.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})


@login_required
def user_list(request):
        users = User.objects.filter(is_active=True)\
                    .exclude(username='admin').exclude(username=request.user.username)   #excluding the admin and logged in user from list
        return render(request,
                    'account/user/list.html',
                    {'section': 'people',
                    'users': users})

@login_required
def user_detail(request, username):
        user = get_object_or_404(User,
                                username=username,
                                is_active=True)
        return render(request,
                    'account/user/detail.html',
                    {'section': 'people',
                    'user': user})



@ajax_required
@require_POST
@login_required
def user_follow(request):
        #To get the user_id for user
        user_id = request.POST.get('id')
        #To get the action for user
        action = request.POST.get('action')
        if user_id and action:
            try:
                #The user object who is gets followed
                user = User.objects.get(id=user_id)
                #Check if action is follow
                if action == 'follow':
                    #Create a new object user_from is user who logged in,who follows
                    #user_to the user who is followed by
                    Contact.objects.get_or_create(
                            user_from=request.user,
                            user_to=user)
                    create_action(request.user, 'is following', user)
                else:
                    #Unfollow case
                    #Filter based on user_from and user_to,delete the relation
                    Contact.objects.filter(user_from=request.user,user_to=user).delete()
                #if no exception set status to ok
                return JsonResponse({'status':'ok'})
            except User.DoesNotExist:
                return JsonResponse({'status':'ko'})
        #if no user_id or action ,status ko
        return JsonResponse({'status':'ko'})
