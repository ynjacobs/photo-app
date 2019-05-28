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
  # this is where we'll receive the form submission
  pass
  

