# django-related-models

django-related-models adds a Related Models sidebar to admin pages for easy navigation to related join fields. It supports both ForeignKey fields and ManyToMany relationships linking both ways.

# Usage

Include it in your `INSTALLED_APPS` in settings before `django.contrib.admin`:
```
    INSTALLED_APPS = [
        ...
        'django_related_models',
        'django.contrib.admin',
        ...
    ]
```

A sidebar will now showup on admin edit pages.

### For reverse ManyToMany relationships
