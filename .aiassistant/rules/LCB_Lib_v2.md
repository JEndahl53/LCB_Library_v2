---
apply: always
---

Project Rules – Community Band Library
You are an expert in Python, Django, and scalable web application development.
You write secure, maintainable, and performant code that follows the rules in this document. 
When working on this project:
    * Prefer explaining options and tradeoffs before making changes.
    * Propose changes as patches/diffs and ask for confirmation before applying them.
    * Follow the project's existing patterns and libraries unless explicitly asked to change them. 
    * When providing code suggestions, include the filepath.
Python
    * Follow PEP 8 with a 120-character line limit.
    * Use double quotes for Python strings.
    * Use isort-style sorted imports (standard lib, third-party, local).
    * Use f-strings for string formatting. 
When suggesting new modules:
    * Include minimal, focused functions and classes.
    * Prefer readability to cleverness. 
Django – General
    * Follow Django's "batteries included" philosophy; use built-ins before third-party packages.
    * Prioritize security and Django's security best practices.
    * Use the Django ORM; avoid raw SQL unless absolutely necessary and clearly documented.
    * Use signals sparingly and document them when used.
    * Use get_user_model() instead of importing User directly.
    * Prefer path() over re_path() in URLconfs unless regex is clearly required. 
Models
    * Add __str__ methods to all models to improve the admin and debugging.
    * Use related_name for foreign keys where appropriate.
    * Use a Meta class for options such as ordering and verbose_name.
    * Use blank=True for optional form fields, null=True for optional DB fields.
    * Implement soft deletion using an is_active BooleanField (standard in this project).
    * For models with custom clean(), call full_clean() in save(). 
When designing new models:
    * Ensure relationships support referential navigation for roles and organizations.
    * Design so that adding new person roles or organization types is easy and does not require schema changes. 
Views & Interaction
    * Use function-based views (FBVs) instead of CBVs.
    * Always validate and sanitize user input.
    * Use get_object_or_404 for lookups instead of manual exception handling.
    * Implement proper pagination for list views. 
HTMX
    * Use HTMX for dynamic content: live search, filtering, partial updates.
    * HTMX views must return partial templates (prefixed with _) when the HX-Request header is present.
    * Partial templates should be named with a leading underscore, e.g.  _person_table.html. 
If JavaScript is needed beyond HTMX:
    * Alpine.js is available; use it only when necessary. 
URLs
    * Use descriptive URL names for reverse lookups.
    * End URL patterns with a trailing slash.
    * Namespace URLs for each app (e.g. library:list, concerts:detail). 
Forms
    * Use ModelForms when working with model instances.
    * Use django-widget-tweaks to integrate forms with Tailwind/DaisyUI. 
When generating new forms:
    * Include basic validation and error messaging.
    * Keep business logic out of form clean() methods unless specific to that field. 
Templates
    * Use template inheritance with base templates.
    * Use template tags/filters for reusable or complex logic.
    * Avoid putting complex logic in templates; move it to views or template tags.
    * Use {% load static %} and Django's static files correctly.
    * Ensure all forms include CSRF protection. 
For HTMX:
    * Use partial templates (leading _) for fragments.
    * Make partials focused on a single responsibility (e.g., table body, row, filter form). 
Settings & Environment
    * Use a single settings.py with environment-dependent values driven by env vars.
    * Never commit secrets to VCS.
    * Use django-environ for environment variable management. 
Runtime assumptions:
    * All databases are PostgreSQL (local, staging, production).
    * Production runs in Docker with gunicorn, caddy, and postgres.
    * There is a staging server running in parallel with production, also using Postgres. 
    * Development postgres is run on the local machine, not in a Docker container.
Database & Querying
    * Use migrations for all DB changes.
    * Use select_related and prefetch_related to avoid N+1 problems.
    * Add indexes to frequently queried fields, especially is_active and search fields.
    * Maintain referential integrity for role-based link tables (MusicRole, ConcertRole, OrganizationRole, etc.). 
Testing
    * Always write tests for new features and bug fixes.
    * Use pytest and pytest-django.
    * Test both positive and negative paths.
    * Prefer TestCase for DB-dependent tests unless pytest fixtures are specifically needed.
    * Mock external services and APIs.
    * Ensure views are covered with status code and basic content assertions. 
Architecture & Project-Specific Rules
Domain overview
This is a Django-based online library and concert tracker for a community band. 
Access levels
    * Public: library, concert, and people list and detail pages.
    * Band members: accounts created using django-allauth, allows access to linked recordings.
    * Band librarian: editing access via front-end CRUD and in-line adds.
    * Admin site: superuser-only.
    * Band members are not stored in the Person model/table. 
Library section
    * Track at least: title, composer, arranger, publisher, location, copyright date, duration. Title is the only required field.
    * Support basic and expanded list views; clicking a list item opens a detail view. 
Concert section
    * Track at least: date, location, performers, concert program, notes, concert title. Date, location/venue, and concert title are required fields
    * Concert detail includes:
        * Pieces performed in performance order.
        * Links to recordings for members.
        * Item statistics (performance history, counts of compositions, concerts, etc.). 
Other domain entities
    * Organizations: loaning/borrowing/renting/publishing organizations.
    * Persons: composers, arrangers, conductors, guests.
    * Use role/link tables (e.g., MusicRole, ConcertRole, OrganizationRole) to represent roles and relationships, designed so new roles/types can be added without schema changes. 
UI & UX
    * The project must be mobile-friendly and responsive.
    * Lists should support live search and filtering (prefer HTMX with django-filter).
    * During early development, do not incorporate Tailwind; apply CSS later.
    * Librarian should have a full CRUD interface for all tables in the database (except User). There should also be an option to do in-line additions of data when entering new records (i.e. librarian starts to enter a new concert and discovers the concert venue is missing from the venue table. The interface provides in-line to add the venue, so the concert-creation process is not interrupted. New entries added this way should have the "needs review" flag set to 'on' by default)
Libraries & Tools
Use these libraries when relevant:
    *  django-tailwind for Tailwind CSS (later in the project).
    *  DaisyUI as the Tailwind component library.
    *  django-debug-toolbar for debugging.
    *  django-extensions for management commands.
    *  django-widget-tweaks for forms.
    *  django-environ for env vars.
    *  django-filter for filtering.
    *  Font Awesome Free for icons.
    *  pytest-django for tests.
    *  HTMX for dynamic interactions; Alpine.js if strictly necessary. 
Architecture guideline:
    * Use a services layer (e.g., people/services/) for complex business logic; keep views thin.
    * Provide basic functionality first, with the expectation that the final project will use Tailwind CSS, DaisyUI, and HTMX for the user interface.
