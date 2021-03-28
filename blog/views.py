from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CommentCreateForm, PostSearchForm, PostCreateForm, TagCreateForm, CategoryCreateForm
from .models import Post, Comment, Tag, Category
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView  # 追記
from django.contrib.auth.forms import UserCreationForm  # 追記
from django.urls import reverse_lazy  # 追記
from . import forms


class LoginPostList(generic.ListView):
    template_name = "blog/login_post_list.html"
    model = Post
    ordering = "-created_at"
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PostSearchForm(self.request.GET or None)
        # ↓の２行でログインユーザの記事を絞り込み可能
        if self.request.user.is_authenticated:
            queryset = queryset.filter(writer=self.request.user)
        if form.is_valid():
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                queryset = queryset.filter(Q(title__icontains=key_word) | Q(text__icontains=key_word))

            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

            tags = form.cleaned_data.get('tags')
            if tags:
                queryset = queryset.filter(tags__in=tags).distinct()

            user = form.cleaned_data.get('user')
            # writerモデルの外部キー(django組み込みuserモデル)のusernameフィールドで記事投稿者の絞りこみ。
            if user:
                queryset = queryset.filter(writer__username__icontains=user)

        return queryset


class PostList(generic.ListView):
    model = Post
    ordering = "-created_at"
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PostSearchForm(self.request.GET or None)
        if form.is_valid():
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                queryset = queryset.filter(Q(title__icontains=key_word) | Q(text__icontains=key_word))

            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

            tags = form.cleaned_data.get('tags')
            if tags:
                queryset = queryset.filter(tags__in=tags).distinct()

            user = form.cleaned_data.get('user')
            # 外部キー(django組み込みuserモデル)のusernameフィールドで絞り込み。
            if user:
                queryset = queryset.filter(writer__username__icontains=user)

        return queryset


class PostDetail(generic.DetailView):
    model = Post


class LoginPostDetail(generic.DetailView):
    template_name = "blog/login_post_detail.html"
    model = Post


class CommentCreate(generic.CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.save()
        return redirect("blog:post_detail", pk=post_pk)


class PostCategoryList(generic.ListView):
    model = Post
    ordering = "-created_at"
    paginate_by = 4

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs["pk"])
        return super().get_queryset().filter(category=category)


class PostTagList(generic.ListView):
    model = Post
    ordering = "created_at"
    paginate_by = 4

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs["pk"])
        return super().get_queryset().filter(tags=tag)


class PostCreate(generic.CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy("blog:post_list")

    # ログインしているユーザ名をwriterモデルに自動で追加
    def form_valid(self, form):
        # commit=Falseを入れることで保存前のインスタンスを生成
        instance = form.save(commit=False)
        # ユーザ情報追加
        instance.writer = self.request.user
        # 保存(タグ以外)
        instance.save()
        # タグがManyToManyなので以下が必要
        form.save_m2m()
        return redirect('blog:post_list')


class TagCreate(generic.CreateView):
    template_name = 'blog/tag_form.html'
    form_class = TagCreateForm
    success_url = reverse_lazy("blog:post_create")


class CategoryCreate(generic.CreateView):
    template_name = 'blog/category_form.html'
    form_class = CategoryCreateForm
    success_url = reverse_lazy("blog:post_create")


class PostUpdate(generic.UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = "blog/post_update.html"
    success_url = reverse_lazy("blog:post_list")


class PostDelete(generic.DeleteView):
    model = Post
    success_url = reverse_lazy("blog:post_list")


class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "blog/account_login.html"


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "blog/account_logout.html"
    success_url = reverse_lazy("blog:post_list")


class IndexView(TemplateView):
    template_name = "blog/account_index.html"


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "blog/account_create.html"
    success_url = reverse_lazy("blog:login")
