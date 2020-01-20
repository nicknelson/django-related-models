# django-related-models

django-related-models adds a Related Models sidebar to admin pages for easy navigation to related join fields. It supports both ForeignKey fields and ManyToMany relationships linking both ways.

# Installation

Install django-related-models with pip:
```
    pip install django-related-models
```

Include it in your `INSTALLED_APPS` in settings:
```
    INSTALLED_APPS = [
        ...
        'django_cache_tags'
    ]
```

A sidebar will now showup on admin edit pages.

### For reverse ManyToMany relationships
