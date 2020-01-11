from django.contrib import admin, messages
from django.core.exceptions import FieldError
from django.db.models import ForeignKey, ManyToManyField, ManyToManyRel, Model
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from urllib.parse import quote, urlencode


class ModelAdmin(admin.ModelAdmin):
    exclude_during_duplication = ()
    additional_related_models = []

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

    def fields_as_params(self, obj):
        fields_to_ignore = {
            'id',
            'oid'
        }
        fields_to_ignore = fields_to_ignore.union(self.readonly_fields)
        fields_to_ignore = fields_to_ignore.union(self.exclude_during_duplication)
        fields = model_to_dict(obj)
        for field, value in list(fields.items()):
            if field in fields_to_ignore or not value:
                del fields[field]
            else:
                if type(fields[field]) in [list]:
                    for i, item in enumerate(fields[field]):
                        if isinstance(item, Model):
                            fields[field][i] = str(item.id)
                    fields[field] = ",".join(fields[field])
        return urlencode(fields, True)

    def response_add(self, request, obj, post_url_continue=None):
        if "_addandcopy" in request.POST:
            opts = obj._meta
            preserved_filters = self.get_preserved_filters(request)
            obj_url = reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(obj.pk,),
                current_app=self.admin_site.name,
            )
            if self.has_change_permission(request, obj):
                obj_repr = format_html('<a href="{}">{}</a>', quote(obj_url), obj)
            else:
                obj_repr = str(obj)
            msg_dict = {
                'name': opts.verbose_name,
                'obj': obj_repr,
            }
            msg = format_html(
                _('The {name} "{obj}" was added successfully. You may add another {name} below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url += '?' + self.fields_as_params(obj)
            redirect_url = admin.templatetags.admin_urls.add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        else:
            return super(ModelAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if "_addandcopy" in request.POST:
            opts = self.model._meta
            preserved_filters = self.get_preserved_filters(request)
            msg_dict = {
                'name': opts.verbose_name,
                'obj': format_html('<a href="{}">{}</a>', quote(request.path), obj),
            }
            msg = format_html(
                _('The {name} "{obj}" was changed successfully. You may add another {name} below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:%s_%s_add' %
                                   (opts.app_label, opts.model_name),
                                   current_app=self.admin_site.name)
            redirect_url += '?' + self.fields_as_params(obj)
            redirect_url = admin.templatetags.admin_urls.add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
            return super(ModelAdmin, self).response_change(request, obj)

    def get_foreign_key_relationship(self, related_model, object_id):
        query_fields = {
            f'{self.model._meta.model_name}': object_id
        }
        related_objects = related_model.objects.filter(**query_fields)
        model_name = related_model._meta.model_name[0].upper() + related_model._meta.model_name[1:]
        related_fields = f'<strong>{model_name}</strong><ul>'
        if related_objects.count() > 10:
            related_fields += f'<li><a href="{reverse(f"admin:{related_model._meta.app_label}_{related_model._meta.model_name}_changelist")}?{self.model._meta.model_name}_id={object_id}">See all {related_objects.count()} {model_name}s</a></li>'
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
                related_fields += f'<li><a href="{reverse(f"admin:{related_model._meta.app_label}_{related_model._meta.model_name}_change", args=(o.id,))}">{label}</a></li>'
        related_fields += '</ul>'
        return related_fields

    def related_fields(self, object_id):
        show_related_objects_in = [
            # add related models here
        ]
        related_fields = ''
        obj = self.model.objects.get(id=object_id)
        if self.model in show_related_objects_in:
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
                        related_fields += '<strong>' + field.name[0].upper() + field.name[1:] + '</strong><ul style="margin-left:1rem">'
                        for v in values:
                            model_name = v._meta.app_label + '_' + v._meta.model_name
                            related_fields += f'<li><a href="{reverse(f"admin:{model_name}_change", args=(v.id,))}">{str(v)}</a></li>'
                        related_fields += '</ul>'

            for related_model in self.additional_related_models:
                related_fields += self.get_foreign_key_relationship(related_model, object_id)

            return mark_safe(related_fields)
