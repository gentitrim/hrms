from django.contrib import admin
from .models import BranchManager,Branch
# Register your models here.
admin.site.register(BranchManager)
admin.site.register(Branch)