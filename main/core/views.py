from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
 

 
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Post, Category

from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    template_name = 'bit/index.html'

def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    return render(request, 'core/detail.html', {'post': post, 'form': form})

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)

    return render(request, 'core/category.html', {'category': category, 'posts':posts})

def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) |Q(body__icontains=query))

    return render(request, 'core/search.html', { 'posts': posts, 'query': query})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        
        if form.is_valid():
            user = form.save() 
            login(request, user)
            messages.success(request, "Registration successful." )
            
            return render(request, 'bit:index.html')

        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    return render (request=request, template_name="bit/register.html", context={"register_form":form})
 
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return render(request, 'bit:index.html')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="bit/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('bit:index.html')




