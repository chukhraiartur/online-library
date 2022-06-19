from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return HttpResponse("The testapp view.")

def books(request, bookid):
    return HttpResponse(f"<h1>The book {bookid} view.</h1>")

def archive(request, year):
    if int(year) == 2022:
        return redirect('home', permanent=False)
    if int(year) > 2022:
        raise Http404()
    return HttpResponse(f"<h1>The books {year} view.</h1>")

def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Oops...</h1>")