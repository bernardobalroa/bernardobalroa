# src/core/rbac_models.py
# Placeholder for Role-Based Access Control (RBAC) related models
# Assuming a Python/Django-like ORM structure for now

class Permission:
    """
    Defines a specific permission in the system.
    Permissions are granular actions that can be performed on resources.
    e.g., "create_task", "edit_task_status", "view_client_billing", "manage_users"
    """
    # id: int (Primary Key)
    # name: str (A unique codename for the permission, e.g., "task.create", "client.view.all")
    #         # Convention: resource.action[.scope]
    # description: str (User-friendly description, e.g., "Can create new tasks", "Can view all client data")
    # resource: str (The entity this permission pertains to, e.g., "task", "client", "user", "system_settings")
    # action: str (The action allowed, e.g., "create", "read", "update", "delete", "approve", "assign")
    # created_at: datetime
    # updated_at: datetime
    pass

class RolePermission:
    """
    Joins Roles to Permissions (Many-to-Many relationship).
    This table assigns specific permissions to roles.
    """
    # id: int (Primary Key)
    # role_id: int (Foreign Key to Role model in src/users/models.py)
    # permission_id: int (Foreign Key to Permission model)
    #
    # # Optional: Add constraints or conditions if a permission for a role is conditional
    # # condition: str (e.g., "is_owner" - though this can get complex, often handled in application logic)
    pass

# Note on Role model:
# The Role model itself is defined in src/users/models.py.
# It would have a many-to-many relationship with Permission, likely through this RolePermission table.
# Example (in Role class in users/models.py):
# permissions = relationship("Permission", secondary="role_permissions_table_name", backref="roles")

# This structure allows:
# 1. Defining a set of available permissions system-wide.
# 2. Creating roles (like "Editor", "Manager").
# 3. Assigning a subset of these permissions to each role.
# 4. Assigning users to roles.
#
# Application logic would then check:
# Does user X have role Y? Does role Y have permission Z for resource W?
#
# Example Permissions:
# - ("task.create", "Create new tasks")
# - ("task.edit.own", "Edit tasks assigned to self")
# - ("task.edit.all", "Edit any task for assigned clients")
# - ("task.delete", "Delete tasks")
# - ("task.change_status.review", "Change task status to 'In Review'")
# - ("client.view.assigned", "View details of assigned clients")
# - ("client.edit.assigned", "Edit details of assigned clients")
# - ("user.manage", "Manage users and roles (Admin)")
# - ("social.post.schedule", "Schedule social media posts")
# - ("content.approve", "Approve edited content")
