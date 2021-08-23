from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import EmailPostForm
from django.core.mail import send_mail
from .models import Comment
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count
def post_list(request,category=None, tag_slug=None):
    object_list=Post.published.all()
    tag = None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator=Paginator(object_list,1)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'post/list.html',{'posts':posts,'page':page, 'tag': tag})

def post_detail(request, year, month, day, post):
    post=get_object_or_404(Post,slug=post,
                           status='published',
                           publish__year=year,
                           publish__month=month,
                           publish__day=day
                           )

    comments=post.comments.filter(active=True)
    new_comment=None
    if request.method == 'POST':
        form = CommentForm(data=request.POST)

        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post

            new_comment.save()

    else:
        form=CommentForm()

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]


    return render(request,'post/detail.html',{'post':post, 'comments':comments, 'new_comment':new_comment, 'form':form,
                                              'similar_posts': similar_posts})



def post_share(request, post_id):
# Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'post/share.html', {'post': post,
                                               'form': form,
                                               'sent': sent})

