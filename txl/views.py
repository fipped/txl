from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
@csrf_exempt
def page_not_found(request):
    return render_to_response('base.html')


@csrf_exempt
def page_error(request):
    return render_to_response('base.html')