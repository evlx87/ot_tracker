from django.db import models

class Department(models.Model):
    name = models.CharField("Подразделение / Цех / Отдел", max_length=150, unique=True)
    def __str__(self): return self.name

class Position(models.Model):
    name = models.CharField("Должность / Профессия", max_length=150)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="positions")
    def __str__(self): return f"{self.name} ({self.department})"

class Employee(models.Model):
    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    patronymic = models.CharField("Отчество", max_length=100, blank=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name="employees")
    hire_date = models.DateField("Дата приёма")
    is_active = models.BooleanField("В штате", default=True)

    # Флаги освобождений (соответствуют колонкам файла)
    exempt_primary_briefing = models.BooleanField("Освобождён от первичного инструктажа", default=False)
    exempt_internship = models.BooleanField("Не требуется стажировка на рабочем месте", default=False)
    exempt_ot_training = models.BooleanField("Освобождён от обучения по ОТ", default=False)

    class Meta:
        ordering = ["position__department", "position", "last_name"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self): return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self): return f"{self.last_name} {self.first_name} {self.patronymic}".strip()
