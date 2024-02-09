from django.contrib import admin
from .models import PatientRecords, Conctact


# Register your models here.
class PatientRecordsAdmin(admin.ModelAdmin):
    list_display = ["patient", "pred_class", "score", "image", "desc"]


admin.site.register(PatientRecords, PatientRecordsAdmin)


class ConctactAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "tel", "subject", "message"]


admin.site.register(Conctact, ConctactAdmin)
