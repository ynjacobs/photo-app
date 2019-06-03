from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from photogur.models import Picture, Comment
from django.urls import reverse
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



def picture(request):
    comments = Comment.objects.all()
    pictures = Picture.objects.all()
    
    for picture in pictures:
        no_comments = 0
        for comment in comments:
            if comment.picture.title == picture.title:
                no_comments += 1
        picture.no_comments = no_comments
    
    context = {'pictures': pictures}
    
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def root(request):
    return HttpResponseRedirect('/admin')

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def picture_search(request):
  query = request.GET['query']
  search_results = Picture.objects.filter(artist=query)
  context = {'pictures': search_results, 'query': query}
  response = render(request, 'bunch.html', context)
  return HttpResponse(response)

def create_comment(request):
    comment_title = request.POST['comment_title']
    comment_msg = request.POST['comment_message']
    pic_id = request.POST['picture']
    new_comment_pic = Picture.objects.get(id = pic_id)
    comment = Comment(name=comment_title, message=comment_msg, picture=new_comment_pic)
    comment.save()
    print('title', comment_title,'-' ,'msg:', comment_msg,'pic', new_comment_pic)
    # return HttpResponseRedirect(reverse('picture'))
    return redirect('picture_details', id= pic_id)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('pictures')
    else:
        form = UserCreationForm()
    html_response =  render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

@login_required
def add_pic(request):
    if request.method == 'POST':
        picture = Picture(user = request.user)
        picture.user = request.user
        form = PictureForm(request.POST, instance=picture)
        if form.is_valid():
            add_pic = form.save()
            return HttpResponseRedirect('/pictures')
        else:
            context = { 'form': form }
            response = render(request, 'add_pics.html', context)
            return HttpResponse(response)
    else:
        form = PictureForm()
        context = { 'form': form }
        response = render(request, 'add_pics.html', context)
        return HttpResponse(response)


