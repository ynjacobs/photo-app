from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from photogur.models import Picture, Comment

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

