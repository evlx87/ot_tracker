from django.db.models import Count, Q
from employees.models import Employee
from training.models import TrainingRecord, TrainingCategory

def calculate_matrix_summary(active_only=True):
    qs = Employee.objects.select_related("position")
    if active_only:
        qs = qs.filter(is_active=True)

    total = qs.count()
    exempt_ot = qs.filter(exempt_ot_training=True).count()
    no_internship = qs.filter(exempt_internship=True).count()
    exempt_briefing = qs.filter(exempt_primary_briefing=True).count()

    # Подлежащие обучению ППП и СИЗ (исключаем освобождённых от ОТ, если они не учатся по другим программам)
    # В вашем файле ППП и СИЗ считаются отдельно, поэтому берём всех активных
    ppp_count = total
    siz_count = total  # В реальности лучше фильтровать по PositionTrainingRequirement

    return {
        "total_ot": total,
        "exempt_ot": exempt_ot,
        "no_internship": no_internship,
        "exempt_briefing": exempt_briefing,
        "ppp": ppp_count,
        "siz": siz_count,
    }