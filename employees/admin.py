from django.contrib import admin
from .models import Department, Position, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "department")
    search_fields = ("name", "department__name")
    list_filter = ("department",)
    autocomplete_fields = ("department",)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "position", "hire_date", "is_active")
    search_fields = ("last_name", "first_name", "patronymic", "position__name")
    list_filter = ("is_active", "position__department")
    autocomplete_fields = ("position",)