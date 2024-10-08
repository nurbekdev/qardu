from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic import ListView

from category.models import get_permission_queryset
from oauth.models import Teacher
from posts.forms import PostForm, PublicPostForm
from posts.models import Post

# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

class PublishPostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["pk"])
        post.is_published = not post.is_published
        post.save()
        return redirect("post_public:my_list")

def delete_post_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    messages.success(request, "Пост успешно удален")
    return redirect("post_public:my_list")



class PostListAdminView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 10
    template_name = "administrator/posts/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = get_permission_queryset(self.request.user).filter(
            is_delete=False
        )
        context["teacher_list"] = Teacher.objects.all()
        return context

    def get_queryset(self):
        posts = Post.objects.filter(
            category__in=get_permission_queryset(self.request.user)
        )

        category = self.request.GET.get("category")
        name = self.request.GET.get("name")
        select_data = self.request.GET.get("select-data")

        if category:
            posts = posts.filter(category=category)

        if name:
            posts = posts.filter(
                Q(title__icontains=name)
                | Q(teacher__first_name__icontains=name)
                | Q(teacher__last_name__icontains=name)
                | Q(teacher__father_name__icontains=name)
            )

        if select_data:
            order_options = {
                "date-publications-desc": "-date",
                "date-publications-asc": "date",
                "date-created-desc": "-created",
                "date-created-asc": "created"
            }
            order_by = order_options.get(select_data)
            if order_by:
                posts = posts.order_by(order_by)

        return posts


def post_create_update_view(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
        title = _("Редактировать публикацию")
    else:
        post = None
        title = _("Добавить публикацию")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_admin:list")
        else:
            message_error = "Пожалуйста, исправьте следующие ошибки:\n"
            for field in form:
                if field.errors:
                    message_error += f"{field.label}: {field.errors}\n"
            messages.error(request, message_error)
    else:
        form = PostForm(instance=post)

    return render(request, "administrator/posts/form.html", {"form": form, "title": title})


class PostListPublicView(ListView):
    template_name = "public/posts/list.html"
    model = Post
    paginate_by = 12

    def get_queryset(self):
        queryset = Post.objects.all()
        group_id = self.request.GET.get("group")
        select_data = self.request.GET.get("select-data")

        if group_id:
            try:
                queryset = queryset.filter(category__group_id=group_id)
            except ValueError:
                pass

        order_options = {
            "date-publications-desc": "-date",
            "date-publications-asc": "date",
            "date-created-desc": "-created",
            "date-created-asc": "created"
        }
        order_by = order_options.get(select_data)
        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset


class PostDetailPublicView(generic.DetailView):
    template_name = "public/posts/detail.html"
    model = Post


class PublishPostView(LoginRequiredMixin, generic.TemplateView):
    template_name = "public/posts/publish.html"

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs["pk"])
        post.is_published = not post.is_published
        post.save()
        return self.get(request, *args, **kwargs)


def delete_post_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    messages.success(request, "Пост успешно удален")
    return redirect("posts:list")


class PostOwnListPublicView(ListView):
    template_name = "public/posts/own_list.html"
    model = Post
    paginate_by = 20

    def get_queryset(self):
        queryset = Post.objects.filter(teacher=self.request.user.teacher)
        select_data = self.request.GET.get("select-data")

        order_options = {
            "date-publications-desc": "-date",
            "date-publications-asc": "date",
            "date-created-desc": "-created",
            "date-created-asc": "created",
            "status-desc": "-status",
            "status-asc": "status"
        }
        order_by = order_options.get(select_data)
        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PublicPostForm
    template_name = "public/posts/form.html"

    def form_valid(self, form):
        form.instance.teacher = self.request.user.teacher
        form.instance.status = 1
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_public:my_list")


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PublicPostForm
    template_name = "public/posts/form.html"

    def get_queryset(self):
        return Post.objects.filter(teacher=self.request.user.teacher)

    def get_success_url(self):
        return reverse("post_public:my_list")
