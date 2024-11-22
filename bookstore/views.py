from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import git


@csrf_exempt
def update(request):
    if request.method == "POST":
        try:
            repo = git.Repo('/home/sezimarjr/bookstore')
            origin = repo.remotes.origin
            pull_info = origin.pull()
            return HttpResponse(f"Updated code on PythonAnywhere: {pull_info}")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")


def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())
