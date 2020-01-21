from django.contrib import admin
from django.core.exceptions import FieldError
from django.db.models import ForeignKey, ManyToManyField, ManyToManyRel
from django.forms.models import model_to_dict
from django.urls import reverse


class ModelAdmin(admin.ModelAdmin):
    exclude_during_duplication = ()
    additional_related_models = []
    hide_related = False

    def change_view(self, request, object_id, **kwargs):
        related_fields = self.related_fields(object_id)
        context = {
            'related_fields': related_fields
        }
        if 'extra_context' in kwargs.keys():
            kwargs['extra_context'].update(context)
        else:
            kwargs['extra_context'] = context
        return super(ModelAdmin, self).change_view(request, object_id, **kwargs)

    def get_foreign_key_relationship(self, related_model, object_id, field=None):
        field_name = field if field else self.model._meta.model_name
        query_fields = {
            f'{field_name}': object_id
        }
        related_objects = related_model.objects.filter(**query_fields)
        model_name = related_model._meta.verbose_name.title()
        related_fields = {
            'header': model_name,
            'fields': list()
        }
        if related_objects.count() > 10:
            related_fields['fields'].append({
                'url': f'{reverse(f"admin:{related_model._meta.app_label}_{related_model._meta.model_name}_changelist")}?{self.model._meta.model_name}_id={object_id}',
                'name': f'See all {related_objects.count()} {model_name}s'
            })
        else:
            for o in related_objects:
                if o._meta.model_name == 'occurrence':
                    label = str(o.location)
                elif o._meta.model_name == 'schedule':
                    schedule_dates = []
                    for rule in o.dates.rrules:
                        schedule_dates.append(rule.to_text())
                    for date in o.dates.rdates:
                        schedule_dates.append(date.astimezone().strftime('%b %-d'))
                    label = f'{", ".join(schedule_dates)}, {o.start_time}'
                else:
                    label = str(o)
                related_fields['fields'].append({
                    'url': f'{reverse(f"admin:{related_model._meta.app_label}_{related_model._meta.model_name}_change", args=(o.id,))}',
                    'name': label
                })
        return related_fields

    def related_fields(self, object_id):
        related_fields = list()
        obj = self.model.objects.get(id=object_id)
        if not self.hide_related:
            fields = obj._meta.get_fields(include_parents=True)
            this_obj = model_to_dict(obj)

            for field in fields:
                if type(field) in [ManyToManyField, ForeignKey, ManyToManyRel]:
                    if type(field) == ManyToManyRel:
                        field_model = field.remote_field.model
                        field_name = field.remote_field.name
                        kwargs = {
                            '{0}'.format(field_name): obj
                        }
                        try:
                            values = list(field_model.objects.filter(**kwargs))
                        except FieldError:
                            values = []
                    elif type(field) == ForeignKey:
                        try:
                            values = [field.remote_field.model.objects.get(id=this_obj[field.name])]
                        except field.remote_field.model.DoesNotExist:
                            values = []
                    elif type(field) in [ManyToManyField]:
                        values = [x for x in this_obj[field.name]]
                    if len(values) > 0:
                        this_fields = list()
                        for v in values:
                            model_name = v._meta.app_label + '_' + v._meta.model_name
                            this_fields.append({
                                'url': reverse(f"admin:{model_name}_change", args=(v.id,)),
                                'name': str(v)
                            })
                        related_fields.append({
                            'header': field.verbose_name.title() if hasattr(field, 'verbose_name') else field.name.title(),
                            'fields': this_fields
                        })

            for related_model in self.additional_related_models:
                m, f = related_model
                related_fields.append(self.get_foreign_key_relationship(m, object_id, field=f))

            return related_fields
