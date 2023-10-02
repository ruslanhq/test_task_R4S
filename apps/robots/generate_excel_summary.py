import openpyxl

from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

from apps.robots.models import Robot


def generate_excel_summary(request):
    wb = openpyxl.Workbook()

    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=7)

    robots = Robot.objects.filter(
        created__gte=start_date,
        created__lte=end_date
    ).values('model').distinct()
    if not robots:
        return HttpResponse(
            "No robot production data available for the last week."
        )

    # Create a worksheet for each model
    for model_data in robots:
        model_name = model_data['model']
        ws = wb.create_sheet(title=model_name)
        ws.append(['Model', 'Version', 'Number per week'])

        # Query the database for production totals for this model
        model_production = Robot.objects.filter(
            model=model_name,
            created__gte=start_date,
            created__lte=end_date
        ).values('version').annotate(total=Count('id'))

        # Write production data to the worksheet
        for data in model_production:
            ws.append([model_name, data['version'], data['total']])

    # Remove the default worksheet
    default_sheet = wb.get_sheet_by_name('Sheet')
    wb.remove(default_sheet)

    # Create a response with the Excel content
    response = HttpResponse(content_type='application/ms-excel')
    response[
        'Content-Disposition'
    ] = 'attachment; filename="robot_production_summary.xlsx"'
    wb.save(response)
    return response
