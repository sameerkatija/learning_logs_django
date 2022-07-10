from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout , authenticate, login
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm



# Create your views here.
def logout_view(request):
    """Log the user out"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_log:index'))


def register(request):
    """Register a new User"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_log:index'))
    
    context = {'form': form}
    return render(request, 'users/register.html', context)

