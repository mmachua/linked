
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.forms import HomeForm, HomeCreate, ProfileForm
from home.models import Post, Friend
from .models import Create
from home.forms import ContactForm, PostForm
from login.models import UserProfile
from .models import Friend
from django.urls import reverse_lazy
from django.db.models import Count, F, Value
from django.db.models.functions import Length, Upper
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import (ListView, UpdateView, CreateView, FormView, DeleteView)
from django.core.exceptions import ObjectDoesNotExist
from home.models import Post,  Aboutpage, Newsletter
from home.forms import ContactForm, NewsletterForm
from django.contrib.auth.decorators import login_required


from django.http import JsonResponse

# ...


from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from .forms import HomeForm, NewsletterForm

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post
from .forms import PostForm

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'home/home.html'

    def has_user_liked_post(self, user, post):
        return post.likes.filter(pk=user.pk).exists()

    def get(self, request, pk=None):
        form = PostForm()
        posts = Post.objects.all().order_by('-date')

        for post in posts:
            post.is_liked = self.has_user_liked_post(request.user, post)

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {'form': form, 'posts': posts}
        return render(request, self.template_name, context)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home:home')
        else:
            # Handle form validation errors here if needed
            pass

        posts = Post.objects.all().order_by('-date')
        context = {'form': form, 'posts': posts}
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class LikePostView(View):
    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
            user = request.user

            # Check if the user has already liked the post
            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
            else:
                post.likes.add(user)
                liked = True

            # Save the post
            post.save()

            return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

# @method_decorator(login_required, name='dispatch')
# class HomeView(TemplateView):
#     template_name = 'home/home.html'

#     # Define the has_user_liked_post method within the class
#     def has_user_liked_post(self, user, post):
#         return post.likes.filter(pk=user.pk).exists()

#     def get(self, request, pk=None):
#         form = HomeForm()
#         posts = Post.objects.all().order_by('-date')

#         for post in posts:
#             post.is_liked = self.has_user_liked_post(request.user, post)

#         paginator = Paginator(posts, 10)
#         page = request.GET.get('page')
#         try:
#             posts = paginator.page(page)
#         except PageNotAnInteger:
#             posts = paginator.page(1)
#         except EmptyPage:
#             posts = paginator.page(paginator.num_pages)

#         context = {'form': form, 'posts': posts}
#         return render(request, self.template_name, context)

#     def post(self, request):
#     # Handle the post form submission
#         form = PostForm(request.POST, request.FILES)  # Include request.FILES for image upload

#         if form.is_valid():
#             post = form.save(commit=False)  # Remove 'commit=False'
#             post.user = request.user
#             post.save()
#             return redirect('home:home')  # Redirect to the home page after successful submission
#         else:
#             # Handle form validation errors here if needed
#             pass

#         # If the form is not valid, you can render the same page with the form and error messages
#         posts = Post.objects.all().order_by('-date')
#         context = {'form': form, 'posts': posts}
#         return render(request, self.template_name, context)


def load_more_posts(request):
    page = request.GET.get('page')
    paginator = Paginator(Post.objects.all().order_by('-date'), 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        return JsonResponse({'home/home.html': ''})  # No more posts

    context = {'posts': posts}
    posts_html = render_to_string('home/posts_partial.html', context)  # Create a partial HTML template for posts
    return JsonResponse({'home/post': posts_html})





#postdetail view
class Post_detailView(TemplateView):
    template_name = 'home/detail.html'

    def get(self, request, id, pk=None):

        if pk:
            post = get_object_or_404(Post, id=id, available=True)
        else:
            post = get_object_or_404(Post, id=id, available=True)

        args = {'post':post}

        return render(request, self.template_name, args)


def like_post(request):
    post = get_object_or_404( Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())    

@login_required
def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
        return redirect('home:memelords')
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:memelords') 









#class AboutView(TemplateView):
#    template_name = 'home/About.html'  





#contact form views are here
def contact(request):
    form_class = ContactForm(request.POST or None)

    return render(request, 'home/contact.html', {
        'form': form_class,
    })


@method_decorator(login_required, name='dispatch')
class PostFormView(LoginRequiredMixin, CreateView):
    template_name = 'home/post.html'
    model = Post
    form_class = PostForm
    #fields = '__all__'
    success_url = reverse_lazy('login:view_profile')
    #user = User
    
 
    def form_valid(self, form):
        post = form.cleaned_data.get('post')
        
        image1 = form.cleaned_data.get('image1')
        
        form.instance.user = self.request.user
        
        return super().form_valid(form)#, context)


 
from login.models import UserProfile
from home.forms import ProfileForm

from django.views.generic.edit import UpdateView

@method_decorator([login_required], name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'home/updateprofile.html'
    model = UserProfile
    success_url = reverse_lazy('login:view_profile')
    form_class = ProfileForm

    def get_object(self):
        try:
            return UserProfile.objects.get(User=self.request.user)
        except ObjectDoesNotExist:
            print("UserProfile not found for this user.")
            return None  # You may want to handle this case differently

    def form_valid(self, form):
        user_profile = self.get_object()
        if user_profile:
            form.instance.User = user_profile.User  # Set the User field in the form instance
            return super(ProfileUpdateView, self).form_valid(form)
        else:
            print("UserProfile not found for this user.")
            return super(ProfileUpdateView, self).form_invalid(form)



class AboutView(TemplateView):
    template_name = 'home/about.html'


    def get(self, request):
        aboutpages = Aboutpage.objects.all()

        args = {
            'aboutpages': aboutpages
        }
        return render(request, self.template_name, args)

@method_decorator([login_required], name='dispatch')
class MemeLordsView(TemplateView):
    template_name = 'home/memelords.html'
    
    def get(self, request):
        # Check if a Friend object exists for the current user
        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
        except Friend.DoesNotExist:
            # If it doesn't exist, create one
            friend = Friend.objects.create(current_user=request.user)
            friends = []

        query = request.GET.get('q')
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query)  # Add more fields as needed
            )
        else:
            users = User.objects.exclude(id=request.user.id)

        args = {
            'users': users,
            'friend': friend,
            'friends': friends
        }
        return render(request, self.template_name, args)
