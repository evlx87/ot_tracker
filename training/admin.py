from django.contrib import admin
from .models import TrainingProgram, TrainingRecord

@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ("employee", "program", "training_date", "expiry_date", "is_expired")
    list_filter = ("program", "is_planned")
    search_fields = ("employee__last_name", "certificate_number")
    autocomplete_fields = ("employee", "program")

    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = "Просрочено"