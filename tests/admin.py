from django.contrib import admin
from django_related_models.admin import ModelAdmin
from tests.models import ModelCentral, ModelA, ModelB, ModelFK, ModelMM


class ModelAAdmin(ModelAdmin):
    model = ModelA


class ModelBAdmin(ModelAdmin):
    model = ModelB


class ModelCentralAdmin(ModelAdmin):
    model = ModelCentral


class ModelFKAdmin(ModelAdmin):
    model = ModelFK


class ModelMMAdmin(ModelAdmin):
    model = ModelMM


admin.site.register(ModelCentral, ModelCentralAdmin)
admin.site.register(ModelA, ModelAAdmin)
admin.site.register(ModelB, ModelBAdmin)
admin.site.register(ModelFK, ModelFKAdmin)
admin.site.register(ModelMM, ModelMMAdmin)
