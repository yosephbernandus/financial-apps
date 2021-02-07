from enum import Enum


class PermissionType(Enum):
    # We can't have nested enum, so we put it flat
    VIEW_USER = "View User"
    VERIFY_USER = "Verify User"
    ADD_USER = "Add User"
    EDIT_USER = "Edit User"

