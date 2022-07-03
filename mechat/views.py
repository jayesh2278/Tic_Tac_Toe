from django.http import HttpResponse
from django.shortcuts import render
from .forms import joinform

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = joinform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            roomname = form.cleaned_data['roomname']
            return render(request, 'index.html', {'username': username, 'roomname': roomname})
        else:
            return HttpResponse(' form not ok')

    else:
        form = joinform()
        return render(request, 'detail.html', {'form':form})
    