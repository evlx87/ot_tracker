from django.views.generic import TemplateView
from django.db.models import Prefetch
from employees.models import Employee
from training.models import TrainingRecord, TrainingCategory
from django.http import HttpResponse
from .exports import export_training_matrix_excel

class TrainingMatrixView(TemplateView):
    template_name = "training/matrix.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        employees = (Employee.objects
        .filter(is_active=True)
        .select_related("position__department")
        .prefetch_related(
            Prefetch("training_records",
                     queryset=TrainingRecord.objects.filter(is_archived=False).order_by('-training_date'))
        ))

        matrix = {}
        for emp in employees:
            latest = {}
            for rec in emp.training_records.all():
                if rec.category not in latest:
                    latest[rec.category] = rec
            matrix[emp.id] = latest

        programs = [{"code": code, "name": name} for code, name in TrainingCategory.choices]

        ctx.update({
            "programs": programs,
            "employees": employees,
            "matrix": matrix,
        })
        return ctx

def download_matrix(request):
    wb = export_training_matrix_excel()
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="учет_обучения.xlsx"'
    wb.save(response)
    return response
