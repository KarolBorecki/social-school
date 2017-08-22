from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from groups.forms import PostCreateForm, CommentCreateForm, GroupCreateForm
from .models import Group, GroupMember, Post, Comment


class GroupListView(LoginRequiredMixin, generic.ListView):
    model = Group

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['groups'] = self.request.user.user_groups.all()
        return context


class GroupIndexView(LoginRequiredMixin, generic.DetailView):
    template_name = 'groups/group_main_page.html'
    form_class = PostCreateForm
    context_object_name = 'group'

    def get_queryset(self):
        return Group.objects.all()

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


class AddPostView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'groups/post_detail.html'
    form_class = CommentCreateForm
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(AddPostView, self).get_context_data(**kwargs)
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


class AddUserToGroupView(LoginRequiredMixin, generic.ListView):
    template_name = 'groups/add_user_to_group.html'
    model = GroupMember
    context_object_name = 'group_members'

    def get_context_data(self, **kwargs):
        context = super(AddUserToGroupView, self).get_context_data(**kwargs)
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        context['group_members'] = group.members.all()
        return context

    def post(self, request, *args, **kwargs):

        if 'add_users' in request.POST:
            users_primary_keys = request.POST.getlist('user_id', False)
            group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
            print(users_primary_keys)
            for pk in users_primary_keys:
                user = User.objects.filter(pk=pk).get()
                GroupMember.objects.create(user=user, group=group)

            return HttpResponseRedirect(reverse('groups:group_timeline', kwargs={'slug': self.kwargs.get('slug')}))


class CreateGroupView(LoginRequiredMixin, generic.View):
    template_name = 'groups/group_create_form.html'
    form_class = GroupCreateForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']

            group = Group(name=name, description=description)
            group.save()

            return HttpResponseRedirect(reverse('groups:join_group', kwargs={'slug': group.slug}))
        else:
            return render(request, self.template_name, {'form': form})


class JoinGroupView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:group_timeline', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

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
        return reverse('groups:index', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
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

