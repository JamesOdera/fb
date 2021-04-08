from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.forms import modelformset_factory
from django.template.loader import render_to_string
from django.db.models import Q


def index(request):
    posts = Post.objects.all()
    profiles = Profile.objects.all()

    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(author__username=query) |
            Q(body__icontains=query)
        )

    context = {
        'posts': posts,
        'profiles': profiles,
    }
    return render(request, 'index.html', context)


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(
                post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    context = {
        'is_liked': is_liked,
        'post': post,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
    }
    if request.is_ajax():
        html = render_to_string(
            'app/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'app/post_detail.html', context)


def like_post(request):
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'post': post,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string(
            'app/like_section.html', context, request=request)
        return JsonResponse({'form': html})
    # return HttpResponseRedirect(post.get_absolute_url())


def post_create(request):
    ImageFormset = modelformset_factory(Images, fields=('image',))
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = (request.user)
            post.save()

            for form in formset:
                try:
                    photo = Images(post=post, image=form.cleaned_data['image'])
                    photo.save()

                except Exception as e:
                    break
            return redirect('index')
    else:
        form = PostCreateForm()
        formset = ImageFormset(queryset=Images.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'app/post_create.html', context)


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    ImageFormset = modelformset_factory(Images, fields=('image',), max_num=1)
    if post.author != request.user:
        raise Http404()
    if request.method == 'POST':
        form = PostEditForm(request.POST or None, instance=post)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            form.save()

            data = Images.objects.filter(post=post)
            for index, form in enumerate(formset):
                if form.cleaned_data:
                    if form.cleaned_data['id'] is None:
                        photo = Images(
                            post=post, image=form.cleaned_data['image'])
                        photo.save()
                    elif form.cleaned_data['image'] is False:
                        photo = Images.objects.get(
                            id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()
                    else:
                        photo = Images(
                            post=post, image=form.cleaned_data['image'])
                        d = Images.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
        formset = ImageFormset(queryset=Images.objects.filter(post=post))
    context = {
        'form': form,
        'post': post,
        'formset': formset,
    }
    return render(request, 'app/post_edit.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    post.delete()
    return redirect('index')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('User is not Active')
            else:
                return HttpResponse('User is None')
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'app/login.html', context)


def fb_login(request):
    context = {}
    return render(request, 'app/fb_login.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'app/register.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('edit_profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'app/edit_profile.html', context)
