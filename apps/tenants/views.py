from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from .models import User, Company, CompanySubscription
from .forms import CompanyUserCreationForm

class SignUpView(CreateView):
    form_class = CompanyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ProfileView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'tenants/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'tenants/company_detail.html'

    def get_object(self):
        return self.request.user.company

class CompanyUpdateView(UpdateView):
    model = Company
    fields = ['name', 'address', 'phone', 'email', 'tax_id']
    template_name = 'tenants/company_form.html'
    success_url = reverse_lazy('company_detail')

    def get_object(self):
        return self.request.user.company

class UserListView(ListView):
    model = User
    template_name = 'tenants/user_list.html'

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)

class UserDetailView(DetailView):  # <-- Добавленный класс
    model = User
    template_name = 'tenants/user_detail.html'
    context_object_name = 'user_object'

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)

class UserCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'role', 'is_company_admin']
    template_name = 'tenants/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'role', 'is_company_admin']
    template_name = 'tenants/user_form.html'
    success_url = reverse_lazy('user_list')

class SubscriptionDetailView(DetailView):
    model = CompanySubscription
    template_name = 'tenants/subscription_detail.html'

    def get_object(self):
        return self.request.user.company.subscription