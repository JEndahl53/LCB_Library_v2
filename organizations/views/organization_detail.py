# organizations/views/organization_detail.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404

from organizations.models import Organization
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def organization_detail(request, pk):
    org = get_object_or_404(Organization, pk=pk)

    # Get roles for this organization
    roles = org.roles.select_related('role_type').filter(is_active=True)

    # Get music links
    music_links = (
        org.music_links
        .select_related('music', 'role_type')
        .filter(is_active=True)
        .order_by('music__title')
    )

    # Stats
    stats = {
        'total_music': music_links.values('music').distinct().count(),
        'role_counts': {},
    }

    for link in music_links:
        role_name = link.role_type.name
        stats['role_counts'][role_name] = stats['role_counts'].get(role_name, 0) + 1

    context = {
        'org': org,
        'roles': roles,
        'music_links': music_links,
        'stats': stats,
    }

    return render(request, 'organizations/organization_detail.html', context)