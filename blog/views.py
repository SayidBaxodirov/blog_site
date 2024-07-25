from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.core.mail import send_mail
from blog.models import Post
from config import settings
from .forms import CommentForm, EmailPostForm


# Create your views here.
class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, publish_date__year=year, publish_date__month=month, publish_date__day=day)
    comments = post.comment_set.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html',
                  {'post': post, "comment_form": comment_form, "comments": comments, "new_comment": new_comment})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = None
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            link = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} invites you to read post"
            message = f'{cd["name"]} invites you to read post "{post.title}". The link is {link}. Comment by {cd["name"]}: {cd["text"]}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to_email']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post_share.html', {'form': form, 'post': post, 'sent': sent})
