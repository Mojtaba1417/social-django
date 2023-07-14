from django.shortcuts import render, redirect
from django.views import View
from . forms import UserRegistrationForm, UserLoginForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Relation


class RegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, "you regestred successfully", 'success')
            return redirect('home:home')
        return render(request, 'account/register.html', {'form': form})

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserLoginView(View):
    form_class = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)


    def get(self, request):
        form = self.form_class
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:

                login(request, user)
                messages.success(request, "you logged in successfully", 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')

            messages.error(request, "your username or password is wrong", 'danger')
        return render(request, 'account/login.html', {'form': form})


class UserLogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, "you logged out successfully", 'success')
        return redirect('home:home')


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = user.posts.all()
        return render(request, 'account/profile.html', {'user': user, 'posts':posts})


class EditProfileView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        return render(request, 'account/edit_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, "profile edited successfully", 'success')
        return redirect('account:user_profile', request.user.id)


class UserFollowView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(follower=request.user, following=user)
        if relation.exists():
            messages.error(request, f"you already follow {user.username}", 'danger')
        else:
            Relation.objects.create(follower=request.user, following=user)
            messages.success(request, f"you followed {user} successfully", 'success')
        return redirect('account:user_profile', user.id)