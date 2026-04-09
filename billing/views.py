from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Billing
from .forms import BillingForm

class BillingListView(LoginRequiredMixin, ListView):
    model = Billing
    template_name = 'billing/billing_list.html'
    context_object_name = 'bills'
    paginate_by = 20

class BillingDetailView(LoginRequiredMixin, DetailView):
    model = Billing
    template_name = 'billing/billing_detail.html'
    context_object_name = 'bill'

class BillingCreateView(LoginRequiredMixin, CreateView):
    model = Billing
    form_class = BillingForm
    template_name = 'billing/billing_form.html'
    success_url = reverse_lazy('billing:list')

    def form_valid(self, form):
        # Optionally set created_by user if you have a User foreign key
        return super().form_valid(form)

class BillingUpdateView(LoginRequiredMixin, UpdateView):
    model = Billing
    form_class = BillingForm
    template_name = 'billing/billing_form.html'
    success_url = reverse_lazy('billing:list')