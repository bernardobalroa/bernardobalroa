# src/users/models.py
# Placeholder for user and role data models
# Assuming a Python/Django-like ORM structure for now

class Role:
    """
    Represents a user role within the system (e.g., General Manager, Editor).
    """
    # id: int (Primary Key)
    # name: str (e.g., "General Manager", "Editor", "Videographer") - Unique
    # description: str (Optional: A brief description of the role's purpose)
    # permissions: list[Permission] (Many-to-Many relationship with Permission model)
    pass

class User:
    """
    Represents an internal team member or a client user.
    """
    # id: int (Primary Key)
    # email: str (Unique, used for login)
    # password_hash: str (Hashed password)
    # first_name: str (Optional)
    # last_name: str (Optional)
    # role_id: int (Foreign Key to Role model) - Defines the user's role and permissions
    # client_id: int (Foreign Key to Client model, Nullable) - Associates user with a specific client if they are a client user or a team member assigned exclusively.
    #                                                        - Null for general agency staff not tied to one client.
    # is_active: bool (Default: True)
    # created_at: datetime
    # updated_at: datetime
    pass

# Note: Permissions themselves might be defined in a core RBAC model.
# This file focuses on User and Role entities. Relationships to permissions
# will be established through a mapping table or directly in the Role model.
