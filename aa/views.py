from django.shortcuts import get_object_or_404, RequestContext, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from models import Post, Like
from django.contrib.auth.models import User
from forms import PostForm
from ua.models import Member
from ua.models import FollowUser
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import Http404


def home(request):

    args = {}
    args.update(csrf(request))

    if request.user.is_authenticated():

        #info gathering------------------------------------------------------
        m = get_object_or_404(Member, user=request.user.profile)
        p = Post.with_likes.filter(user__in=FollowUser.objects.filter(who=m).values_list('whom')).order_by('-timestamp')

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
        p_in_page = [post.id for post in p]
        l = Like.objects.filter(user=m).filter(post__in=p_in_page).values_list('post__id', flat=True)
    else:
        m = None
        p = None
        l = None

    #packing bags and fly--------------------------------------------------
    args.update({'t': 'Feed', 'p': p, 'l': l})
    template_name = 'posts.html'
    context = RequestContext(request)
    return render_to_response(template_name, args, context_instance=context)


def allpeople(request):

    args = {}
    args.update(csrf(request))

    #info gathering--------------------------------------------------------
    m = get_object_or_404(Member, user=request.user.profile)
    ap = Member.objects.all().order_by('-id')

    #multiple follow stats gathering---------------------------------------------
    if request.user.is_authenticated():

        p_in_page = [p.user for p in ap]
        fed = FollowUser.objects.filter(who=m).filter(whom__in=p_in_page).values_list('whom', flat=True)
    else:
        fed = None

    #packing bags and fly----------------------------------------------------
    args.update({'t': 'All people', 'ap': ap, 'fed': fed})
    template = 'allpeople.html'
    context = RequestContext(request)
    return render_to_response(template, args, context_instance=context)


def allposts(request):

    args = {}
    args.update(csrf(request))

    #info gathering------------------------------------------------------
    p = Post.with_likes.all().order_by('-timestamp')

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
        liked = Like.objects.filter(user=request.user)
        p_in_page = [post.id for post in p]
        liked = liked.filter(post__in=p_in_page)
        l = liked.values_list('post__id', flat=True)
    else:
        l = None

    #packing bags and fly--------------------------------------------------
    args.update({'t': 'All posts', 'p': p, 'l': l})
    template = 'posts.html'
    context = RequestContext(request)
    return render_to_response(template, args, context_instance=context)


def newpost(request):

    args = {}
    args.update(csrf(request))

    #info gathering--------------------------------------------------------
    m = get_object_or_404(Member, user=request.user.profile)

    #making some fun stuff-----------------------------------------------
    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = m
            form.save()

            return HttpResponseRedirect(reverse('allposts'))
    else:
        form = PostForm()

    #packing bags and fly--------------------------------------------------
    args.update({'form': form})
    template = 'newpost.html'
    context = RequestContext(request)
    return render_to_response(template, args, context_instance=context)


@login_required
def editpost(request, post_id):

    args = {}
    args.update(csrf(request))

    #info gathering--------------------------------------------------------
    m = get_object_or_404(Member, user=request.user.profile)
    p = Post.objects.get(id=post_id)

    #making some fun stuff-----------------------------------------------
    if m == p.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=p)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('post', kwargs={"post_id": post_id}))
        else:
            form = PostForm(instance=p)
    else:
        raise Http404

    #packing bags and fly--------------------------------------------------
    args.update({'form': form})
    template = 'editpost.html'
    context = RequestContext(request)
    return render_to_response(template, args, context_instance=context)


def post(request, post_id):

    args = {}
    args.update(csrf(request))

    #info gathering------------------------------------------------------
    p = Post.objects.get(id=post_id)

    #packing bags and fly--------------------------------------------------
    args.update({'p': p})
    template = 'post.html'
    context = RequestContext(request)
    return render_to_response(template, args, context_instance=context)


def deletepost(request, post_id):
    args = {}
    args.update(csrf(request))

    #info gathering--------------------------------------------------------
    m = get_object_or_404(Member, user=request.user.profile)

    p = get_object_or_404(Post, id=post_id, user=m)
    p.delete()

    return HttpResponseRedirect(reverse('home'))


def like(request, target_id):
    target = get_object_or_404(Post, id=target_id)
    if target:
        m = get_object_or_404(Member, user=request.user.profile)
        prev_likes = Like.objects.filter(user=m, post=target)
        has_liked = (len(prev_likes) > 0)
        if not has_liked:
            Like.objects.create(user=m, post=target)
        else:
            prev_likes[0].delete()

    response = HttpResponse(mimetype="text/html")
    response['content-type'] = "text/html; charset=UTF-8"
    response.write('You liked a post "%s"' % target.title)
    return response


def unlike(request, target_id):
    target = get_object_or_404(Post, id=target_id)
    if target:
        m = get_object_or_404(Member, user=request.user.profile)
        prev_likes = Like.objects.filter(user=m, post=target)
        has_liked = (len(prev_likes) > 0)
        if not has_liked:
            Like.objects.create(user=m, post=target)
        else:
            prev_likes[0].delete()

    response = HttpResponse(mimetype="text/html")
    response['content-type'] = "text/html; charset=UTF-8"
    response.write('You unliked a post "%s"' % target.title)
    return response