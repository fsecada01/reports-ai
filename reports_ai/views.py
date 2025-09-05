from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import ReportInstanceForm
from .models import ReportInstance
from .tasks import generate_report_task


class ReportInstanceCreateView(CreateView):
    model = ReportInstance
    form_class = ReportInstanceForm
    template_name = "reports_ai/reportinstance_form.html"

    def get_success_url(self):
        return reverse_lazy("admin:reports_ai_reportinstance_changelist")


class ReportInstanceListView(ListView):
    model = ReportInstance
    template_name = "reports_ai/reportinstance_list.html"
    context_object_name = "reports"


class ReportInstanceDetailView(DetailView):
    model = ReportInstance
    template_name = "reports_ai/reportinstance_detail.html"
    context_object_name = "report"


@staff_member_required
def trigger_report_generation(request, pk):
    generate_report_task.delay(pk)
    return redirect("admin:reports_ai_reportinstance_change", pk=pk)
