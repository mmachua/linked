from django import forms
from home.models import Post, Newsletter
#from django.contrib.auth.models import User
from login.models import UserProfile
from django.conf import settings
User = settings.AUTH_USER_MODEL

class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write a post...'
        }
    ))
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ('post','image')

class HomeCreate(forms.ModelForm):
    bizname = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write the business name here...'
        }
    ))
    location = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write the location of the business here...'
        }
    ))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write the phone number to your business here...'
        }
    ))

class ContactForm(forms.Form):
    Name = forms.CharField(required=True,max_length=25, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your name here 25 characters max...'
        }
    ))
    Email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your email address here...'
        }
    ))
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your message here...'
        }
    
    ))
    

#class ContactForm(forms.ModelForm):
#    contact_name = forms.CharField(required=False, max_length=100)
#    contact_email = forms.EmailField(required=True)


class PostForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write the Caption...'
        }
    ))
    image1 = forms.ImageField()

    class Meta:
        model = Post
        fields = [
            'post',
            
            'image1'
          
        ]
    
    # def save(self, user=None):
    #     post = super(PostForm, self).save(commit=True)
    #     if User:
    #         post.User = user
    #     post.save()
    #     return post
    #         #Post.save()
    #     #return Post
         




class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            'phone',
            'image',
            'city',
            'description',
            #'website',
        ]

    # def save(self, user=None):
    #     userprofile = super(ProfileForm, self).save(commit=False)  # Set commit=False to prevent saving immediately
    #     if user:
    #         userprofile.user = user  # Use lowercase 'user' instead of 'User'
    #     userprofile.save()
    #     return userprofile




class NewsletterForm(forms.ModelForm):

    attrs={
        'class':'form-control',
        'placeholder': 'Write your email here...'
    }
    class Meta:
        model = Newsletter
        fields = [
            'email'
        ]