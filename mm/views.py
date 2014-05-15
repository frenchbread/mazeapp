from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext


def amap(request):

    context_vars = {}
    context_vars.update(csrf(request))

    #packing bags and fly--------------------------------------------------
    context = RequestContext(request)
    template = 'map.html'
    return render_to_response(template, context_vars, context_instance=context)
