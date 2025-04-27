from django.shortcuts import render, redirect, get_object_or_404
from .models import Branch
from branch_management.models import BranchStaff
from user_authentication.forms import CustomUserRegisterForm
from user_authentication.models import CustomUser
from .forms import BranchForm, ManagerForm, CustomManagerUpdateForm, EmployeeUpdateForm
from django.views.generic import (
    TemplateView,
    ListView,
    FormView,
    DeleteView,
    UpdateView,
    DetailView,
    View,
)
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q, F, ExpressionWrapper, FloatField, Sum
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.utils.timezone import now, timedelta
from hrms.rolemixin import RoleAccessMixin
from restaurant.models import Order
from user_authentication.forms import CustomUserResetPassForm
import calendar


class OwnerDashboardView(LoginRequiredMixin, RoleAccessMixin, TemplateView):
    model = Branch
    template_name = "management/owner_dashboard.html"
    allowed_roles = ["admin"]

    def get_context_data(self, **kwargs):
        today = now().date()
        context = super().get_context_data(**kwargs)
        # Get the total number of branches
        context["total_branches"] = Branch.objects.count()
        # Get the total number of managers
        context["total_managers"] = BranchStaff.objects.filter(role="manager").count()
        # Get the total number of staff
        context["total_staff"] = BranchStaff.objects.filter(
            Q(role="staff") | Q(role="manager")
        ).count()
        # Get the total number of orders
        daily_order = Order.objects.filter(order_time__date=today).count()
        context["total_orders"] = daily_order
        # Get the total revenue

        daily_total = (
            Order.objects.filter(order_time__date=today).aggregate(Sum("total_price"))[
                "total_price__sum"
            ]
            or 0
        )
        context["total_revenue"] = daily_total / 100
        return context


class MainPage(LoginRequiredMixin, RoleAccessMixin, TemplateView):
    allowed_roles = ["admin"]
    template_name = "management/main.html"


class BranchListView(LoginRequiredMixin, RoleAccessMixin, ListView):
    allowed_roles = ["admin"]
    paginate_by = 3
    model = Branch
    template_name = "management/branches_list.html"
    ordering = ["name"]

    def get_queryset(self):
        today = now().date()
        search_query = self.request.GET.get('search', '')
        
        # Base queryset with annotations
        branches = Branch.objects.annotate(
            raw_turnover=Sum(
                "branch__order__total_price",
                filter=Q(
                    branch__order__order_time__date=today,
                    branch__order__status="CONFIRMED",
                ),
            ),
            daily_turnover=ExpressionWrapper(
                F("raw_turnover") / 100.0, 
                output_field=FloatField()
            ),
        ).order_by("name")

        # Apply search filter if search query exists
        if search_query:
            branches = branches.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        # Add manager information to each branch
        for branch in branches:
            manager = (
                BranchStaff.objects.filter(branch=branch, role="manager")
                .select_related("user")
                .first()
            )
            branch.manager = manager

        return branches

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the search query back to template to maintain the search term in input
        context['search_query'] = self.request.GET.get('search', '')
        return context


class CreateBranchView(LoginRequiredMixin, RoleAccessMixin, FormView):
    allowed_roles = ["admin"]
    template_name = "management/create_branch.html"
    success_url = reverse_lazy("main_management:branch")
    form_class = BranchForm

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        try:
            Branch.objects.create(
                name=cleaned_data["name"],
                address=cleaned_data["address"],
                phone=cleaned_data["phone"],
                email=cleaned_data["email"],
            )
            messages.success(self.request, "Branch created successfully!")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, "Error creating branch: {}".format(e))
            return HttpResponse(f"Error: {e}", status=500)

    def form_invalid(self, form):
        messages.error(
            self.request, "Error creating branch. Please check the form and try again."
        )
        return super().form_invalid(form)


class SearchBranchView(LoginRequiredMixin, RoleAccessMixin, ListView):
    allowed_roles = ["admin"]
    template_name = "management/branches_list.html"
    paginate_by = 3
    model = Branch
    context_object_name = "branches"

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        if search:
            return Branch.objects.filter(Q(name__icontains=search)).order_by("name")
        return Branch.objects.all().order_by("name")


class EditBranchView(LoginRequiredMixin, RoleAccessMixin, UpdateView):
    allowed_roles = ["admin"]
    model = Branch
    template_name = "management/edit_branch.html"
    success_url = reverse_lazy("main_management:branch")
    form_class = BranchForm

    def form_valid(self, form):
        messages.success(self.request, "Branch updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Error updating branch. Please check the form and try again."
        )
        return super().form_invalid(form)


class DeleteBranchView(LoginRequiredMixin, RoleAccessMixin, DeleteView):
    model = Branch
    allowed_roles = ["admin"]
    template_name = "management/delete_branch.html"
    success_url = reverse_lazy("main_management:branch")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "TEST MESSAGE - BEFORE DELETE")
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Branch deleted successfully.")
            return response
        except Exception as e:
            messages.error(request, f"Failed to delete branch: {e}")
            return redirect(self.success_url)


class BranchDetailView(LoginRequiredMixin, RoleAccessMixin, DetailView):
    allowed_roles = ["admin"]
    model = Branch
    template_name = "management/branch_detail.html"
    context_object_name = "branch"

    def get_object(self, queryset=None):
        return get_object_or_404(Branch, id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)

        weekly_total_revenue = (
            Order.objects.filter(
                order_time__date__range=(week_start, week_end)
            ).aggregate(Sum("total_price"))["total_price__sum"]
            or 0
        )

        context["weekly_total_revenue"] = weekly_total_revenue / 100

        month_start = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        month_end = today.replace(day=last_day)

        monthly_total_revenue = (
            Order.objects.filter(
                order_time__date__range=(month_start, month_end)
            ).aggregate(Sum("total_price"))["total_price__sum"]
            or 0
        )

        context["monthly_total_revenue"] = monthly_total_revenue / 100

        return context


class ManagerListView(LoginRequiredMixin, RoleAccessMixin, ListView):
    allowed_roles = ['admin']
    model = BranchStaff
    template_name = 'management/manage_manager.html'
    context_object_name = 'managers'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = BranchStaff.objects.filter(role='manager').select_related('user', 'branch')
        
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(branch__name__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )
        
        return queryset.order_by('user__last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class CreateManagerView(LoginRequiredMixin, RoleAccessMixin, View):
    allowed_roles = ["admin"]
    template_name = "management/create_manager.html"
    success_url = reverse_lazy("main_management:manager_list")

    def get(self, request):
        managerform = ManagerForm()
        userform = CustomUserRegisterForm()
        return render(
            request,
            self.template_name,
            {"managerform": managerform, "userform": userform},
        )

    def post(self, request):
        managerform = ManagerForm(request.POST)
        userform = CustomUserRegisterForm(request.POST)
        if managerform.is_valid() and userform.is_valid():
            user = userform.save(commit=False)
            user.save()
            manager = managerform.save(commit=False)
            manager.user = user
            manager.role = "manager"
            manager.save()
            messages.success(request, "Manager created successfully!")
            return redirect(self.success_url)

        if managerform.errors:
            if managerform.errors:
                messages.error(request, f"Manager form errors: {managerform.errors}")
            if userform.errors:
                messages.error(request, f"User form errors: {userform.errors}")
        if userform.errors:
            messages.error(request, "Please complete in the correct form.")
            return render(
                request,
                self.template_name,
                {"managerform": managerform, "userform": userform},
            )

        return render(
            request,
            self.template_name,
            {"manager_errors": managerform.errors, "user_errors": userform.errors},
        )


class ManagerUpdateView(LoginRequiredMixin, RoleAccessMixin, View):
    allowed_roles = ["admin"]
    template_name = "management/manager_edit.html"
    success_url = reverse_lazy("main_management:manager_list")

    def get(self, request, pk):
        manager = get_object_or_404(BranchStaff, pk=pk)
        managerform = ManagerForm(instance=manager)
        userform = CustomManagerUpdateForm(instance=manager.user)
        return render(
            request,
            self.template_name,
            {"managerform": managerform, "userform": userform, "manager": manager},
        )

    def post(self, request, pk):
        manager = get_object_or_404(BranchStaff, pk=pk)
        managerform = ManagerForm(request.POST, instance=manager)
        userform = CustomManagerUpdateForm(request.POST, instance=manager.user)
        if managerform.is_valid() and userform.is_valid():
            user = userform.save()
            manager = managerform.save(commit=False)
            manager.user = user
            manager.save()
            messages.success(request, "Manager updated successfully!")
            return redirect(self.success_url)

        if managerform.errors:
            messages.error(request, "Please complete in the correct form.")
        if userform.errors:
            messages.error(request, "Please complete in the correct form.")
            return render(
                request,
                self.template_name,
                {"managerform": managerform, "userform": userform},
            )
        return render(
            request,
            self.template_name,
            {
                "managerform": managerform,
                "userform": userform,
                "manager": manager,
            },
        )


class ManagerDeleteView(LoginRequiredMixin, RoleAccessMixin, View):
    allowed_roles = ["admin"]
    template_name = "management/manager_delete.html"
    success_url = reverse_lazy("main_management:manager_list")

    def get(self, request, pk):
        manager = get_object_or_404(BranchStaff, pk=pk)
        return render(request, self.template_name, {"manager": manager})

    def post(self, request, pk):
        manager = get_object_or_404(BranchStaff, pk=pk)
        user = manager.user
        manager.delete()
        user.delete()
        messages.success(request, "Manager deleted successfully!")

        return redirect(self.success_url)


class ManagerDetailView(LoginRequiredMixin, RoleAccessMixin, DetailView):
    allowed_roles = ["admin"]
    model = BranchStaff
    template_name = "management/manager_detail.html"
    context_object_name = "manager"

    def get_object(self, queryset=None):
        return get_object_or_404(BranchStaff, id=self.kwargs.get("pk"))


class ManagerResetPasswordView(LoginRequiredMixin, RoleAccessMixin, View):
    allowed_roles = ["admin"]
    template_name = "management/reset_password.html"
    login_url = reverse_lazy("user_authentication:login")
    next = reverse_lazy("lo")

    def get(self, request, pk):
        staff_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserResetPassForm()
        return render(
            request, self.template_name, {"form": form, "staff_user": staff_user}
        )

    def post(self, request, pk):
        staff_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserResetPassForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            staff_user.set_password(new_password)
            staff_user.save()
            messages.success(
                request, f"Password for {staff_user.username} has been changed."
            )
            return redirect("main_management:manager_list")  # or any page you want
        return render(
            request, self.template_name, {"form": form, "staff_user": staff_user}
        )


class AllEmployeesListView(ListView):
    model = BranchStaff
    paginate_by = 5
    template_name = "management/all_employees_list.html"
    context_object_name = "employees"

    def get_queryset(self):
        return BranchStaff.objects.select_related("user").exclude(role="admin")


class ProfileView(LoginRequiredMixin, RoleAccessMixin, TemplateView):
    allowed_roles = ["admin"]
    template_name = "management/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["branchstaff"] = BranchStaff.objects.filter(
            user=self.request.user
        ).first()
        return context


class EditProfileView(LoginRequiredMixin, RoleAccessMixin, View):
    allowed_roles = ["admin"]
    template_name = "management/edit_profile.html"
    success_url = reverse_lazy("main_management:your_profile")

    def get(self, request, pk):
        staff = get_object_or_404(CustomUser, pk=pk)
        if staff != request.user:
            return HttpResponseForbidden("You are not allowed to edit this profile.")
        user_form = CustomManagerUpdateForm(instance=staff)
        employee_form = EmployeeUpdateForm(instance=staff.branchstaff)
        context = {
            "user_form": user_form,
            "employee_form": employee_form,
            "staff": staff,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        print(request.POST)
        staff = get_object_or_404(CustomUser, pk=pk)
        if staff != request.user:
            return HttpResponseForbidden("You are not allowed to edit this profile.")
        user_form = CustomManagerUpdateForm(request.POST, instance=staff)
        employee_form = EmployeeUpdateForm(request.POST, instance=staff.branchstaff)
        if user_form.is_valid() and employee_form.is_valid():
            user_form.save()
            employee_form.save()
            return redirect(self.success_url)
        if user_form.invalid():
            messages.error(request, "Please correct the errors in the form.")
            return render(
                request,
                self.template_name,
                {
                    "user_form": user_form,
                    "employee_form": employee_form,
                    "staff": staff,
                },
            )
        if employee_form.invalid():
            messages.error(request, "Please correct the errors in the form.")
            return render(
                request,
                self.template_name,
                {
                    "user_form": user_form,
                    "employee_form": employee_form,
                    "staff": staff,
                },
            )

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "employee_form": employee_form,
                "staff": staff,
            },
        )


class ResetPasswordView(LoginRequiredMixin, RoleAccessMixin, View):
    allowed_roles = ["admin"]
    template_name = "management/reset_password.html"
    success_url = reverse_lazy("main_management:your_profile")
    login_url = reverse_lazy("user_authentication:login")
    redirect_field_name = "next"

    def get(self, request, pk):
        staff_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserResetPassForm()
        return render(
            request, self.template_name, {"form": form, "staff_user": staff_user}
        )

    def post(self, request, pk):
        staff_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserResetPassForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            staff_user.set_password(new_password)
            staff_user.save()
            messages.success(
                request, f"Password for {staff_user.username} has been changed."
            )
            return redirect("user_authentication:login")  # or any page you want
        messages.error(request, "Please complete in the correct form.")
        return render(
            request, self.success_url, {"form": form, "staff_user": staff_user}
        )
