from django.db import models
from employees.models import Employee

class ResponsibilityType(models.TextChoices):
    ELECTRICAL = "ELEC", "Ответственный за электрохозяйство"
    FIRE_SAFETY = "FIRE", "Ответственный за пожарную безопасность"

class ResponsibilityRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="responsibilities")
    type = models.CharField("Вид ответственности", max_length=10, choices=ResponsibilityType.choices)
    electrical_group = models.IntegerField("Группа по ЭБ", null=True, blank=True, help_text="Только для электробезопасности")
    order_number = models.CharField("№ приказа о назначении", max_length=50, blank=True)
    valid_from = models.DateField("Действует с")
    valid_until = models.DateField("Действует до")
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Ответственная роль"
        verbose_name_plural = "Ответственные роли"
    