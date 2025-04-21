from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from branch_management.models import BranchStaff
from main_management.models import Branch
from user_authentication.models import CustomUser

class Command(BaseCommand):
    help = "Creates a default branch and an admin user"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Create default branch
        branch, branch_created = Branch.objects.get_or_create(
            name="Default Branch",
            defaults={
                "address": "123 Default St.",
                "phone": "1234567890",
            }
        )
        if branch_created:
            self.stdout.write(self.style.SUCCESS("Default branch created."))
        else:
            self.stdout.write("Default branch already exists.")
        #add to env
        admin_username = "admin"
        admin_password = "admin123" 

        admin_user, user_created = CustomUser.objects.get_or_create(
            username=admin_username,
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                
            }
        )

        if user_created:
            admin_user.set_password(admin_password)
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Admin user created."))
        else:
            self.stdout.write("Admin user already exists.")

        staff_created = False
        if not hasattr(admin_user, 'branchstaff'):
            BranchStaff.objects.create(
                user=admin_user,
                role="admin",
                branch=branch,
                phone="1234567890"
            )
            staff_created = True

        if staff_created:
            self.stdout.write(self.style.SUCCESS("Admin BranchStaff profile created."))
        else:
            self.stdout.write("Admin BranchStaff profile already exists.")
