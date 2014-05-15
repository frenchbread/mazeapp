from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from models import Member, FollowUser
from aa.views import Post, Like
from forms import SettingsForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def profile(request, username):

    context_vars = {}
    context_vars.update(csrf(request))

    #info gathering------------------------------------------------------
    u = get_object_or_404(User, username=username)
    m = Member.objects.get(user=u)
    p = Post.with_likes.filter(user=m).order_by('-timestamp')
    me = Member.objects.get(user=request.user.profile)

    #checking if followed or not-----------------------------------------
    if request.user.username != username:
        try:
            fing = FollowUser.objects.get(who=me, whom=m)
        except:
            fing = None
        if not fing:
            a = 'follow'
        else:
            a = 'unfollow'
    else:
        a = None

    #pagination----------------------------------------------------------
    paginator = Paginator(p, 5)
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    #multiple likes gathering---------------------------------------------
    if request.user.is_authenticated():
        liked = Like.objects.filter(user=me)
        p_in_page = [post.id for post in p]
        liked = liked.filter(post__in=p_in_page)
        l = liked.values_list('post__id', flat=True)
    else:
        l = None

    #packing bags and fly--------------------------------------------------
    context_vars.update({'u': u, 'm': m, 'a': a, 'p': p, 'l': l})
    context = RequestContext(request)
    template = "profile.html"
    return render_to_response(template, context_vars, context_instance=context)


def profileinfo(request, username):

    context_vars = {}
    context_vars.update(csrf(request))

    #info gathering------------------------------------------------------
    u = get_object_or_404(User, username=username)
    m = Member.objects.get(user=u)
    me = Member.objects.get(user=request.user.profile)

    #checking if followed or not-----------------------------------------
    if request.user.username != username:
        try:
            fing = FollowUser.objects.get(who=me, whom=m)
        except:
            fing = None
        if not fing:
            a = 'follow'
        else:
            a = 'unfollow'
    else:
        a = None

    #packing bags and fly--------------------------------------------------
    context_vars.update({'u': u, 'm': m, 'a': a})
    context = RequestContext(request)
    template = 'profileinfo.html'
    return render_to_response(template, context_vars, context_instance=context)


def profilelikes(request, username):

    context_vars = {}
    context_vars.update(csrf(request))

    #info gathering------------------------------------------------------
    u = get_object_or_404(User, username=username)
    m = Member.objects.get(user=u)
    me = Member.objects.get(user=request.user.profile)
    p = Post.with_likes.filter(id__in=Like.objects.filter(user=m).values_list('post__id'))


    #checking if followed or not-----------------------------------------
    if request.user.username != username:
        try:
            fing = FollowUser.objects.get(who=me, whom=m)
        except:
            fing = None
        if not fing:
            a = 'follow'
        else:
            a = 'unfollow'
    else:
        a = None

    #pagination----------------------------------------------------------
    paginator = Paginator(p, 5)
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    #multiple likes gathering---------------------------------------------
    if request.user.is_authenticated():
        liked = Like.objects.filter(user=me)
        p_in_page = [post.id for post in p]
        liked = liked.filter(post__in=p_in_page)
        l = liked.values_list('post__id', flat=True)
    else:
        l = None

    #packing bags and fly--------------------------------------------------
    context_vars.update({'u': u, 'm': m, 'a': a, 'p': p, 'l': l})
    context = RequestContext(request)
    template = "profilelikes.html"
    return render_to_response(template, context_vars, context_instance=context)


def profilefollowing(request, username):

    context_vars = {}
    context_vars.update(csrf(request))

    #info gathering------------------------------------------------------
    u = get_object_or_404(User, username=username)
    m = Member.objects.get(user=u)
    me = Member.objects.get(user=request.user.profile)
    f = Member.objects.filter(user__in=FollowUser.objects.filter(who=m).values('whom'))

    #checking if followed or not-----------------------------------------
    if request.user.username != username:
        try:
            fing = FollowUser.objects.get(who=me, whom=m)
        except:
            fing = None
        if not fing:
            a = 'follow'
        else:
            a = 'unfollow'
    else:
        a = None

    #multiple follow stats gathering---------------------------------------------
    if request.user.is_authenticated():
        p_in_page = [ff.user_id for ff in f]
        fed = FollowUser.objects.filter(who=me).filter(whom__in=p_in_page).values_list('whom', flat=True)
    else:
        fed = None

    #packing bags and fly--------------------------------------------------
    context_vars.update({'u': u, 'm': m, 'a': a, 'f': f, 'fed': fed})
    context = RequestContext(request)
    template = 'profilefollow.html'
    return render_to_response(template, context_vars, context_instance=context)


def profilefollowers(request, username):

    context_vars = {}
    context_vars.update(csrf(request))

    #info gathering------------------------------------------------------
    u = get_object_or_404(User, username=username)
    m = Member.objects.get(user=u)
    me = Member.objects.get(user=request.user.profile)
    f = Member.objects.filter(user__in=FollowUser.objects.filter(whom=m).values('who'))

    #checking if followed or not-----------------------------------------
    if request.user.username != username:
        try:
            fing = FollowUser.objects.get(who=me, whom=m)
        except:
            fing = None
        if not fing:
            a = 'follow'
        else:
            a = 'unfollow'
    else:
        a = None

    #multiple follow stats gathering---------------------------------------------
    if request.user.is_authenticated():
        followed = FollowUser.objects.filter(who=me)
        p_in_page = [ff.user for ff in f]
        followed = followed.filter(whom__in=p_in_page)
        fed = followed.values_list('whom', flat=True)
    else:
        fed = None

    #packing bags and fly--------------------------------------------------
    context_vars.update({'u': u, 'm': m, 'a': a, 'f': f, 'fed': fed})
    context = RequestContext(request)
    template = 'profilefollow.html'
    return render_to_response(template, context_vars, context_instance=context)


@login_required
def follow(request, target_id):
    u = get_object_or_404(User, id=target_id)
    m = Member.objects.get(user=u)
    target = get_object_or_404(Member, user=m)

    response = HttpResponse(mimetype="text/html")
    response['content-type'] = "text/html; charset=UTF-8"

    if target:
        me = get_object_or_404(Member, user=request.user.profile)
        FollowUser.objects.create(who=me, whom=target)
        response.write('You follow %s' % target.user)
    else:
        response.write('Someting went wrong!')

    return response


@login_required
def unfollow(request, target_id):
    target = get_object_or_404(Member, user_id=target_id)

    response = HttpResponse(mimetype="text/html")
    response['content-type'] = "text/html; charset=UTF-8"

    if target:
        me = get_object_or_404(Member, user=request.user.profile)
        last_foll = FollowUser.objects.filter(who=me, whom=target)
        last_foll[0].delete()
        response.write('You dont follow %s' % target.user)
    else:
        response.write('Someting went wrong!')

    return response


@login_required
def settings(request):

    context_vars = {}
    context_vars.update(csrf(request))

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', kwargs={"username": request.user.username}))
    else:
        form = SettingsForm(instance=request.user.profile)

    context_vars.update({'form': form})
    template = 'settings.html'
    context = RequestContext(request)
    return render_to_response(template, context_vars, context_instance=context)