# Django Guidelines

You are an expert in Python, Django, and scalable web application development. You write secure, maintainable, and performant code following Django and Python best practices.

## Python Best Practices
- Follow PEP 8 with a 120-character line limit
- Use double quotes for Python strings
- Sort imports with `isort`
- Use f-strings for string formatting

## Django Best Practices
- Follow Django's "batteries included" philosophy – use built-in features before third-party packages
- Prioritize security and follow Django's security best practices
- Use Django's ORM effectively and avoid raw SQL unless absolutely necessary
- Use Django signals sparingly and document them well.
- Use `get_user_model()` to reference the User model instead of importing `User` directly.
- Prefer `path()` over `re_path()` in URL configurations unless regex is strictly required.

## Models
- Add `__str__` methods to all models for a better admin interface
- Use `related_name` for foreign keys when needed
- Define `Meta` class with appropriate options (ordering, verbose_name, etc.)
- Use `blank=True` for optional form fields, `null=True` for optional database fields
- Implement soft-deletion using an `is_active` BooleanField (standard in this project)
- Use `full_clean()` in the `save()` method for models with custom `clean()` validation logic.

## Views
- Always validate and sanitize user input
- Handle exceptions gracefully with try/except blocks
- Use `get_object_or_404` instead of manual exception handling
- Implement proper pagination for list views
- Use function-based views (FBVs) instead of class-based views (CBVs)
- Use HTMX for dynamic content like live-search, filtering, and partial page updates.
- HTMX views should return partial templates (prefixed with `_`) when `HX-Request` header is present.

## URLs
- Use descriptive URL names for reverse URL lookups
- Always end URL patterns with a trailing slash
- Namespace your URLs for each app (e.g., `app_name:url_name`).

## Forms
- Use ModelForms when working with model instances
- Use `django-widget-tweaks` for rendering form fields with Tailwind CSS/DaisyUI.

## Templates
- Use template inheritance with base templates
- Use template tags and filters for common operations
- Avoid complex logic in templates - move it to views or template tags
- Use static files properly with `{% load static %}`
- Implement CSRF protection in all forms
- Partial templates for HTMX fragments should be named with a leading underscore (e.g., `_person_table.html`).

## Settings
- Use environment variables in a single `settings.py` file
- Never commit secrets to version control
- Use `django-environ` for environment variable management.

## Database
- Use migrations for all database changes
- Optimize queries with `select_related` and `prefetch_related` to avoid N+1 query problems.
- Use database indexes for frequently queried fields (e.g., `is_active`, search fields).
- Ensure referential integrity when using role-based link tables (e.g., `MusicRole`, `ConcertRole`, `OrganizationRole`).

## Testing
- Always write unit tests for new features and bug fixes.
- Use `pytest` and `pytest-django`.
- Test both positive and negative scenarios.
- Prefer `TestCase` for database-dependent tests unless `pytest` fixtures are explicitly needed.
- Mock external services and APIs.
- Ensure all views are covered with status code and content assertions.

## Project specific guidelines

Overview – This project is a Django-based online library and concert tracker for a community band.

### Access levels
- Public can access library and concert lists and detail pages.
- Band members can create accounts which provides access to linked recordings.
- Band librarian has editing access via front-end CRUD pages
- Admin site access is limited to the superuser 

### List views
- Provides basic and expanded views for library and concert lists
- Clicking a specific item in the list view will open a detail view

### Detail views
- Includes all columns for a single selection
- Provides options to the librarian or superuser to edit, delete (inactivate), or add a new item
- Concert detail view includes a listing of performed pieces in performance order, and links to recordings of pieces for members
- Detail pages include item statistics (performance history, number of compositions in the library, total number of concerts, etc.)
- Detail pages should also include some item statistics (performance history, number of compositions in the library, total number of concerts, etc.)

### Library section features
- Tracked information includes: title, composer, arranger, publisher, location, copyright date, duration

### Concert section features
- Tracked information includes: date, location, performers, pieces, notes, concert title

### Other database tables
- Organizations (music-related, such as loaning, borrowing, renting, or publishing organizations)
- Persons (composers, arrangers, conductors, guests). 
- `Django-allauth` is used for site membership. Band members are not part of the people table.


The project needs to be mobile-friendly and responsive. Lists should have live-search and filtering.  

The project should be designed in such a way that adding items such as new person roles or new organization types is straightforward and does not require significant changes to the codebase. Access through linked information should be referential. Additions and role status changes should not require editing the table definitions. 

- Use `django-tailwind` for Tailwind CSS
- DaisyUI is a Tailwind CSS component library
- Use `django-debug-toolbar` for debugging
- Use `django-extensions` for useful commands
- Use `django-widget-tweaks` for form rendering
- Use `django-environ` for environment variables
- Use `django-filter` for filtering
- Use `font awesome free` for icons
- Use `pytest-django` for Django testing
- Use HTMX for dynamic interactions (live search, filtering)
- Alpine.js is available for JavaScript, but only use it when necessary
- In production, this project uses 'gunicorn', 'caddy' and 'postgres'
- In production, the project is deployed in a Docker container.
- There is a staging server that runs in parallel with production, also using 'postgres'
- All databases are postgres
- During early development, do not incorporate tailwind. CSS formatting will be added later.
- Use a services layer for complex business logic (e.g., `people/services/`) to keep views thin.
