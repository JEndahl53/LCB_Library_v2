# people/views/__init__.py

from .person_list import person_list
from .person_detail import person_detail
from .person_add import person_add
from .person_edit import person_edit
from .person_delete import person_delete
from .person_reactivate import person_reactivate
from .role_type_list import role_type_list
from .role_type_add import role_type_add
from .role_type_edit import role_type_edit
from .role_type_delete import role_type_delete

__all__ = [
    'person_list',
    'person_detail',
    'person_add',
    'person_edit',
    'person_delete',
    'person_reactivate',
    'role_type_list',
    'role_type_add',
    'role_type_edit',
    'role_type_delete',
]
