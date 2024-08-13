from django.contrib import admin
from users.models import User

from unfold.admin import ModelAdmin

from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import TextFilter, FieldTextFilter

class CustomTextFilter(TextFilter):
    title = _("Custom filter")
    parameter_name = "query_param_in_uri"

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            # Here write custom query
            return queryset.filter(your_field=self.value())

        return queryset


@admin.register(User)
class CustomAdminClass(ModelAdmin):
    list_filter_submit = True
    list_filter = [
        ("email", FieldTextFilter),
        CustomTextFilter
    ]
    list_display = ["email", "currency", "balance"]