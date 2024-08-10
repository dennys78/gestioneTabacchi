from django.contrib import admin
from .models import descMovimenti

class tipoMovimento(admin.ModelAdmin):
    list_display = ["__str__", "descrizione"]
    search_fields = ["descrizione"]

    class Meta:
        model = descMovimenti


admin.site.register(descMovimenti, tipoMovimento)