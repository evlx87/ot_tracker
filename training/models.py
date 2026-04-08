from django.db import models
from employees.models import Employee
from dateutil.relativedelta import relativedelta
from django.utils import timezone

class TrainingCategory(models.TextChoices):
    OT = "OT", "Охрана труда (Программы А/Б)"
    FIRST_AID = "PP_P", "Первая помощь пострадавшим (ППП)"
    PPE = "SIZ", "Использование СИЗ"
    ELECTRICAL = "ELEC", "Электробезопасность"
    FIRE = "FIRE", "Пожарная безопасность"

class Provider(models.TextChoices):
    EMPLOYER = "EMPLOYER", "Работодатель"
    CENTER = "CENTER", "Учебный центр"

class TrainingRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="training_records")
    category = models.CharField("Категория обучения", max_length=10, choices=TrainingCategory.choices)
    provider = models.CharField("Кто проводил обучение", max_length=10, choices=Provider.choices)
    
    training_date = models.DateField("Дата обучения")
    expiry_date = models.DateField("Действительно до", null=True, blank=True)
    certificate = models.CharField("№ протокола/удостоверения", max_length=100, blank=True)
    
    # Автоматический расчёт срока действия (можно менять по категориям)
    VALIDITY_MONTHS = {"OT": 36, "PP_P": 12, "SIZ": 12, "ELEC": 12, "FIRE": 12}

    class Meta:
        unique_together = ("employee", "category")
        ordering = ["employee", "category"]
        verbose_name = "Запись об обучении"
        verbose_name_plural = "Записи об обучении"

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            months = self.VALIDITY_MONTHS.get(self.category, 12)
            self.expiry_date = self.training_date + relativedelta(months=months)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date() if self.expiry_date else True


class PositionTrainingRequirement(models.Model):
    position = models.ForeignKey("employees.Position", on_delete=models.CASCADE, related_name="required_trainings")
    category = models.CharField("Категория", max_length=10, choices=TrainingCategory.choices)
    
    class Meta:
        unique_together = ("position", "category")
        verbose_name = "Требование к должности"
        verbose_name_plural = "Требования к должностям"
