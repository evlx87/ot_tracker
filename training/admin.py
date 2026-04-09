from django.contrib import admin
from .models import TrainingRecord, PositionTrainingRequirement

@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ("employee", "category", "provider", "training_date", "expiry_date", "is_expired")
    list_filter = ("category", "provider")
    search_fields = ("employee__last_name", "employee__first_name", "certificate")
    autocomplete_fields = ("employee",)

@admin.register(PositionTrainingRequirement)
class PositionTrainingRequirementAdmin(admin.ModelAdmin):
    list_display = ("position", "category")
    list_filter = ("category",)
    search_fields = ("position__name",)
    autocomplete_fields = ("position",)