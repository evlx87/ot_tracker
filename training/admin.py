from django.contrib import admin
from .models import TrainingRecord, PositionTrainingRequirement

@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ("employee", "category", "provider", "training_date", "expiry_date", "is_expired", "is_archived")
    list_filter = ("category", "provider", "is_archived")
    search_fields = ("employee__last_name", "certificate")
    autocomplete_fields = ("employee",)

@admin.register(PositionTrainingRequirement)
class PositionTrainingRequirementAdmin(admin.ModelAdmin):
    list_display = ("position", "category")
    list_filter = ("category",)
    autocomplete_fields = ("position",)