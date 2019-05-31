from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from photogur.models import Picture, Comment
from django.urls import reverse
from photogur.forms import LoginForm



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
    print('tiotle', comment_title,'-' ,'msg:', comment_msg,'pic', new_comment_pic)
    # return HttpResponseRedirect(reverse('picture'))
    return redirect('picture_details', id= pic_id)

def login_view(request):
    form = LoginForm()
    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)

