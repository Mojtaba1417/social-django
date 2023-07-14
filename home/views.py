from django.shortcuts import render, redirect
from django.views import View
from . models import Post, Comment, Vote
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm, PosrSearchForm
from django.utils.text import slugify


class HomeView(View):
    form_class = PosrSearchForm

    def get(self, request):
        posts = Post.objects.order_by('-created')
        # print(request.GET.get('search'), 'aaaaaaaaaaa')
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts': posts, 'form': self.form_class})


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def get(self, request, post_id, post_slug):
        form = self.form_class()
        post = Post.objects.get(pk=post_id, slug=post_slug)
        comments = post.postcomments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and post.user_can_like(request.user):
            can_like = True
        return render(request, 'home/detail.html', {'post': post, 'comments': comments, 'form': form, 'reply_form': self.form_class_reply, 'can_like': can_like})

    def post(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, "your comment sent ", 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "post was deleted successfully ", 'success')
            return redirect('home:home')

        messages.error(request, "you cant not deleted this post", 'danger')
        return redirect('home:home')


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['title'][:20])
            new_post.save()
            messages.success(request, "new post created successfully", 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "you cant not deleted this post", 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:20])
            new_post.save()
            messages.success(request, "new post updated successfully", 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):

        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply= comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "your comment sent successfully", "success")
        return redirect('home:post_detail', post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, "you already liked this post", "danger")
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, "your liked this post", "success")
        return redirect('home:post_detail', post.id, post.slug)