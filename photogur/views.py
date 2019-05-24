from django.http import HttpResponse

def picture(request):
    response = render(request, 'picture.html')
    return HttpResponse(response)