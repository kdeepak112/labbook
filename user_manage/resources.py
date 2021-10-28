from import_export import resources
from .models import uploadExcel

class uploadExcelResources(resources.ModelResource):
    class Meta:
        model = uploadExcel
        