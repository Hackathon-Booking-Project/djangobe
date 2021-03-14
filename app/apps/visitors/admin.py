from django.contrib import admin
from django import forms
from .models import Visitor


class VisitorCreationForm(forms.ModelForm):
    planed_entry = forms.SplitDateTimeField(widget=admin.widgets.AdminSplitDateTime)

    class Meta:
        model = Visitor
        fields = ("first_name", "last_name", "email", "street", "street_no",
                  "city", "postcode", "additional", "department", "planed_entry")


class VisitorChangeForm(forms.ModelForm):
    planed_entry = forms.SplitDateTimeField(widget=admin.widgets.AdminSplitDateTime)
    entry = forms.SplitDateTimeField(
        widget=admin.widgets.AdminSplitDateTime,
        required=False
    )
    outgoing = forms.SplitDateTimeField(
        widget=admin.widgets.AdminSplitDateTime,
        required=False
    )

    class Meta:
        model = Visitor
        fields = ("first_name", "last_name", "email", "street", "street_no",
                  "city", "postcode", "additional", "department", "planed_entry",
                  "entry", "outgoing")


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("key", "department", "planed_entry", "was_present", )
    search_fields = ("key", "email", )
    list_filter = ("department", "was_present", )
    readonly_fields = ("key", "creation_timestamp", )

    def get_form(self, request, obj=None, **kwargs):
        form = VisitorChangeForm
        if not obj:
            form = VisitorCreationForm
        form.user = request.user
        return form

    def get_fieldsets(self, request, obj=None, **kwargs):
        if obj:
            return (
                ("Access", {"fields": ("key", "department")}),
                ("Visitor", {"fields": ("first_name", "last_name", "email", "street",
                                        "street_no", "city", "postcode", )}),
                ("Presence", {"fields": ("planed_entry", "entry", "outgoing",
                                         "creation_timestamp")})
            )
        return (
            ("Access", {"fields": ("department", )}),
            ("Visitor", {"fields": ("first_name", "last_name", "email", "street",
                                    "street_no", "city", "postcode", )}),
            ("Presence", {'classes': ('wide',), "fields": ("planed_entry", )})
        )
