from django.views.generic import TemplateView
from django.db.models import Prefetch
from employees.models import Employee
from training.models import TrainingRecord, TrainingProgram
from django.http import HttpResponse
from .exports import export_training_matrix_excel


class TrainingMatrixView(TemplateView):
    template_name = "training/matrix.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        programs = TrainingProgram.objects.order_by("code")
        
        employees = (Employee.objects
                     .filter(is_active=True)
                     .select_related("position__department")
                     .prefetch_related(
                         Prefetch("training_records", 
                                  queryset=TrainingRecord.objects.select_related("program"))
                     ))
        
        # Формируем словарь: employee_id -> {program_code: record}
        matrix = {}
        for emp in employees:
            matrix[emp.id] = {r.program.code: r for r in emp.training_records.all()}

        ctx.update({
            "programs": programs,
            "employees": employees,
            "matrix": matrix,
        })
        return ctx


def download_matrix(request):
    wb = export_training_matrix_excel()
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="форма_учета_обучения.xlsx"'
    wb.save(response)
    return response
