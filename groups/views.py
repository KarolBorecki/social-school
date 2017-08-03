from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from groups.forms import PostCreateForm, CommentCreateForm
from .models import Group, GroupMember, Post, Comment


class GroupIndexView(generic.DetailView):
    template_name = 'groups/group_main_page.html'
    form_class = PostCreateForm
    model = Group
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super(GroupIndexView, self).get_context_data(**kwargs)
        return context

    def post(self, request,  *args, **kwargs):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            group = Group.objects.filter(slug=self.kwargs.get('slug')).get()
            author = request.user

            post = Post(title=title, text=text, group=group, author=author)
            post.save()

            return HttpResponseRedirect(reverse("groups:post_details", kwargs={'pk': post.id}))
        else:
            return render(request, self.template_name, {'form': form})


class PostView(generic.TemplateView):
    template_name = 'groups/post_detail.html'
    form_class = CommentCreateForm
    model = Group
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.filter(pk=self.kwargs.get('pk')).get()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            text = form.cleaned_data['text']
            post = Post.objects.filter(id=self.kwargs.get('pk')).get()
            author = request.user

            comment = Comment(text=text, post=post, author=author)
            comment.save()
            return HttpResponseRedirect(reverse('groups:post_details', kwargs={'pk': self.kwargs.get('pk')}))
        else:
            return render(request, self.template_name, {'form': form})


class CreateGroupView(LoginRequiredMixin, generic.CreateView):
    model = Group
    fields = ("name", "description")


class GroupListView(LoginRequiredMixin, generic.ListView):
    model = Group


class JoinGroupView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:index", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            messages.warning(
                self.request,
                "Warning, already a member of {}".format(group.name)
            )

        else:
            messages.success(
                self.request,
                "You are now a member of the {} group.".format(group.name)
            )

        return super().get(request, *args, **kwargs)


class LeaveGroupView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:index", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)

