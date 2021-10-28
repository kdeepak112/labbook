from django.contrib import admin
from .models import fileUpload,comment,uploadExcel
# Register your models here.
from import_export.admin import ImportExportModelAdmin

admin.site.register([fileUpload,comment,uploadExcel])

class uploadexcelAdmin(ImportExportModelAdmin):
    list_display = ('field_a','field_b','field_c','field_d')
    