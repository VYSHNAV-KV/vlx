
from django.contrib import admin
from .models import productdb
from .forms import ProductDBForm
from .models import ApprovalMode


@admin.register(productdb)
class ProductAdmin(admin.ModelAdmin):
    form = ProductDBForm  # Use your custom form if applicable


from django.contrib import admin
from .models import ApprovalMode  # Import your model


@admin.register(ApprovalMode)
class ApprovalModeAdmin(admin.ModelAdmin):
    list_display = ['auto_approve']  # Displays the auto_approve field in the list view
    actions = None  # Disables bulk actions (like delete)

    def has_add_permission(self, request):
        # Prevent the addition of more than one ApprovalMode record
        if ApprovalMode.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the ApprovalMode record
        return False



from .models import AdPending, AdApproved, DailyRate

admin.site.register(AdPending)
admin.site.register(AdApproved)
admin.site.register(DailyRate)

# Register your models here.
