from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib.request
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
import frontend.status_codes

experience = "http://127.0.0.1:8001/"

def index(request):
    invalid_login = request.session.pop('invalid_login', False)

    if request.user.is_authenticated():
        return redirect('dashboard')

    return render(request, "index.html", {"invalid_login": invalid_login})

@sensitive_post_parameters()
@csrf_protect
@never_cache
@require_http_methods(["POST"])
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        data = {'username': username, 'password': password}
        url = experience + "autheticate_user/"
        request = urllib.request.Request(url, data=json.dumps(data).encode('utf8'), headers={'content-type': 'application/json'})
        response = (urllib.request.urlopen(request)).read().decode('utf8')
        status = response['status']
        if status == 202:
            return redirect('dashboard')
        else:
            return redirect('index?invalid_login=True')
    return redirect('index')