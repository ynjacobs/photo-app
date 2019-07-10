from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from photogur.models import Picture, Comment
from django.urls import reverse
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


def picture(request):
    comments = Comment.objects.all()
    pictures = Picture.objects.all()

    for picture in pictures:
        no_comments = 0
        for comment in comments:
            if comment.picture.title == picture.title:
                no_comments += 1
        picture.no_comments = no_comments

    return render(request, 'pictures.html', {'pictures': pictures})


def root(request):
    return HttpResponseRedirect('/pictures')


def picture_show(request, id):
    return render(request, 'picture.html', {
        'picture': Picture.objects.get(pk=id)
    })


def picture_search(request):
    query = request.GET['query']

    return render(request, 'search.html', {
        'pictures': search_results,
        'query': Picture.objects.filter(artist=query)
    })


def create_comment(request):
    comment_title    = request.POST['comment_title']
    comment_msg      = request.POST['comment_message']
    pic_id           = request.POST['picture']
    new_comment_pic  = Picture.objects.get(id=pic_id)

    comment = Comment(
        name=comment_title,
        message=comment_msg,
        picture=new_comment_pic
    )

    comment.save()
    return redirect('picture_details', id=pic_id)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username    = form.cleaned_data['username']
            pw          = form.cleaned_data['password']
            user        = authenticate(username=username, password=pw)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')

    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username     = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user         = authenticate(username=username, password=raw_password)

            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})
    


@login_required
def add_pic(request):
    if request.method == 'POST':
        picture      = Picture(user=request.user)
        picture.user = request.user
        form         = PictureForm(request.POST, instance=picture)

        if form.is_valid():
            instance.user = request.user
            add_pic       = form.save()
            return HttpResponseRedirect('/pictures')
        else:
            return render(request, 'add_pics.html', {'form': form})
    else:
        return render(request, 'add_pics.html', {'form': PictureForm() })


@login_required
def edit_picture(request, id):
    picture = get_object_or_404(Picture, id=id, user=request.user.pk)
    picture_form = PictureForm(request.POST, instance=picture)

    if picture_form.is_valid():
        picture_form.save()
        return redirect('picture_details', id=id)
    else:
        return render(request, 'edit_picture.html', {
            'picture_form': picture_form,
            'pic_id': id,
            'error_msg': 'You have invalid form, try again!'
        })
