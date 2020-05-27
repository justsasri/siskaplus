from django.contrib import admin
from django.template.response import TemplateResponse


class ModelAdmin(admin.ModelAdmin):
    """ Add Inspect view feature to ModelAdmin """

    inspect_template = None
    inspect_enabled = False

    def get_urls(self):
        from django.urls import path
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super().get_urls()
        custom_urls = []
        if self.inspect_enabled:
            custom_urls.append(
                path('<path:object_id>/inspect/',
                     self.admin_site.admin_view(self.inspect_view),
                     name='%s_%s_inspect' % info
                     )
            )
        return custom_urls + urls

    def inspect_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        if not self.has_view_or_change_permission(request, obj):
            return PermissionError("You don't have any permissions")
        context = {
            **self.admin_site.each_context(request),
            'self': self,
            'opts': self.opts,
            'instance': obj,
            **(extra_context or {})
        }

        return TemplateResponse(request, self.inspect_template or [
            'admin/%s_%s_inspect.html' % (self.opts.app_label, self.opts.model_name),
            'admin/%s_inspect.html' % self.opts.app_label,
            'admin/inspect.html'
        ], context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)

        if not self.has_view_or_change_permission(request, obj):
            return PermissionError

        if self.has_change_permission(request, obj):
            return self.changeform_view(request, object_id, form_url, extra_context)
        return self.inspect_view(request, object_id, extra_context)
