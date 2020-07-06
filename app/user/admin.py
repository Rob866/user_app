from django.contrib import admin
from user import  models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm,ReadOnlyPasswordHashField
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json
from django.core import serializers


class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Las contraseñas sin procesar no se almacenan, por lo que no hay forma de ver la contraseña de este usuario, "
                    "pero puede cambiar la contraseña mediante este formulario."
                    "<a href=\"../password/\">formulario</a>."))
    class Meta:
        model = models.Usuario
        fields = '__all__'


@admin.register(models.Usuario)
class UserAdmin(DjangoUserAdmin):

    readonly_fields = ['last_login',]
    search_fields = ("email", "nombre", "apellido","username",)
    ordering = ("-date_joined",)

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day

        chart_data = (
            get_user_model().objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        as_json = json.dumps(list(chart_data),cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request,extra_context=extra_context)

    form = CustomUserChangeForm
    fieldsets = (
        ("Credenciales", {"fields": ("username", "password")}),
        (
            "Información Personal",
            {"fields": ("nombre", "apellido","email")},
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Fechas importantes",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","nombre","apellido","email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "nombre",
        "apellido",
        "email"
    )
