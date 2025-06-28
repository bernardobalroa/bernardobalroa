# src/users/services.py
# Placeholder for user and role management business logic

"""
This service layer module will handle the business logic related to users,
roles, and their permissions. It will interact with the data models
(src/users/models.py and src/core/rbac_models.py) and potentially
other services.

Key Functions/Operations to be implemented:

User Management:
- create_user(email, password, role_name, client_id=None, first_name=None, last_name=None)
  - Hash password before saving.
  - Assign role.
  - Associate with a client if client_id is provided (for client users or dedicated agency staff).
  - Handles multi-tenancy: ensures user is created within the correct client scope if applicable.
- get_user_by_id(user_id)
  - Must respect multi-tenancy if the requesting user is not a super-admin.
- get_user_by_email(email)
  - Useful for login and checking for existing users.
- update_user_profile(user_id, first_name=None, last_name=None, ...)
- change_user_password(user_id, old_password, new_password)
- deactivate_user(user_id)
- activate_user(user_id)
- assign_user_to_client(user_id, client_id)
- remove_user_from_client(user_id, client_id) # If users can be associated with multiple clients or reassigned.

Role Management:
- create_role(name, description=None, permissions_names=None)
  - `permissions_names` would be a list of permission codenames (e.g., ["task.create", "client.view.assigned"]).
  - Links Role to Permission objects via the RolePermission join table.
- get_role_by_id(role_id)
- get_role_by_name(name)
- update_role_permissions(role_id, new_permissions_names)
  - Adds/removes permissions associated with a role.
- delete_role(role_id) # Careful: what happens to users with this role? Reassign or block?
- list_roles()

Permission Management (may also be part of core RBAC service):
- list_permissions()
- get_permission_by_name(name) # e.g., "task.create"

Authentication & Authorization:
- authenticate_user(email, password) -> User object or None
  - Checks hashed password.
- check_user_permission(user_id, permission_name, resource_id=None) -> bool
  - This is a crucial function for RBAC.
  - Gets user's role, then checks if the role has the specified permission.
  - `resource_id` might be needed for ownership checks (e.g., can user edit *this specific* task?).
  - Must integrate with multi-tenancy (e.g., permission is checked within current client context).

Utility Functions:
- get_user_permissions(user_id) -> list[Permission]
  - Returns all effective permissions for a user based on their role.

Important Considerations:
- Multi-Tenancy: All operations that deal with users tied to clients or data
  within a client's scope MUST be tenancy-aware. Use `get_current_client_id()`
  from `src/core/multi_tenancy.py` or pass `client_id` explicitly.
- Error Handling: Raise specific exceptions for scenarios like "UserNotFound",
  "RoleNotFound", "PermissionDenied", "InvalidPassword", "EmailAlreadyExists".
- Input Validation: Ensure all inputs are validated (e.g., email format, password strength).
- Password Security: Use strong hashing algorithms (e.g., bcrypt, Argon2).
- Logging: Log important events like user creation, role changes, failed logins.
- Atomic Operations: For operations involving multiple database changes (e.g., creating a user
  and assigning a role), ensure they are atomic (all succeed or all fail). Use database transactions.
"""

# Placeholder function signatures (to be implemented with actual logic)

# --- User Management ---
def create_user(email, password, role_name, client_id=None, first_name=None, last_name=None):
    """
    Creates a new user, hashes their password, and assigns them a role.
    Associates with a client if client_id is provided.
    """
    # 1. Validate input (email format, password strength, role exists).
    # 2. Check if email already exists.
    # 3. Hash password.
    # 4. Find Role object by role_name.
    # 5. If client_id is provided, ensure it's valid and current user has rights to assign to this client.
    # 6. Create User object and save to DB.
    #    - user = User(email=email, password_hash=hashed_password, role_id=role.id, client_id=client_id, ...)
    #    - db.session.add(user)
    #    - db.session.commit()
    # 7. Log creation.
    # 8. Return User object or user_id.

    # Conceptual: Add permission check if creating users is a restricted action
    # if not _check_user_permission(requesting_user_id, "create_user", {"role_name": role_name, "client_id": client_id}):
    #     raise PermissionError("User does not have permission to create new users with this role/client assignment.")

    if not email or not "@" in email: # Very basic email validation
        raise ValueError("Invalid email format.")
    if _get_user_by_email_from_db(email):
        raise ValueError(f"User with email '{email}' already exists.")
    if not password:
        raise ValueError("Password cannot be empty.")

    role = _get_role_by_name_from_db(role_name)
    if not role:
        raise ValueError(f"Role '{role_name}' not found.")

    hashed_password = _hash_password(password)
    new_user_id = _get_next_user_id()

    new_user = {
        "id": new_user_id,
        "email": email,
        "password_hash": hashed_password,
        "role_id": role['id'], # Store role_id
        "client_id": client_id, # Can be None
        "first_name": first_name,
        "last_name": last_name,
        "is_active": True, # Default to active
        # "created_at": datetime.now(), # Conceptual
        # "updated_at": datetime.now()  # Conceptual
    }
    _save_user_to_db(new_user)

    # For safety, often user objects returned from creation don't include password hash
    # However, for mock purposes and further operations, returning it might be okay.
    # Let's return a copy without the hash for this example.
    user_to_return = new_user.copy()
    # del user_to_return["password_hash"] # Or don't delete for mock simplicity

    print(f"User '{email}' (ID: {new_user_id}) created with role '{role_name}'.")
    return user_to_return


def get_user_by_id(user_id, requesting_user_context):
    """
    Retrieves a user by their ID.
    `requesting_user_context` should provide info about the user making the request
    for tenancy and permission checks.
    """
    # 1. Apply multi-tenancy scope if necessary based on requesting_user_context.
    #    If user X from client A tries to get user Y from client B, deny unless super-admin.
    # 2. Fetch user from DB.
    pass

# --- Role Management ---
def create_role(name, description=None, permissions_names=None):
    """
    Creates a new role and assigns specified permissions to it.
    `permissions_names` is a list of permission codenames.
    """
    # 1. Validate input. Check if role name already exists.
    # 2. Create Role object.
    # 3. If permissions_names are provided:
    #    - Fetch Permission objects by their names.
    #    - Create RolePermission entries to link Role and Permissions.
    # 4. Save to DB (atomically).
    # 5. Return Role object or role_id.

    # Conceptual permission check: Does the user (e.g., from requesting_user_context) have permission to create roles?
    # For this mock, we'll assume the check is done by the caller or is implicitly allowed.
    # if not _check_user_permission(requesting_user_id, "manage_roles", {}):
    #     raise PermissionError("User does not have permission to create roles.")

    if not name or not name.strip():
        raise ValueError("Role name cannot be empty.")
    if _get_role_by_name_from_db(name):
        raise ValueError(f"Role with name '{name}' already exists.")

    validated_permission_names = []
    if permissions_names:
        for p_name in permissions_names:
            if p_name not in _MOCK_PERMISSION_DB:
                # In a real app, you might load permissions from a DB table.
                raise ValueError(f"Permission '{p_name}' not found in defined permissions.")
            validated_permission_names.append(p_name)

    new_role_id = _get_next_role_id()
    new_role = {
        "id": new_role_id,
        "name": name,
        "description": description,
        "permissions": validated_permission_names # Storing names directly for mock simplicity
    }
    _save_role_to_db(new_role)
    print(f"Role '{name}' (ID: {new_role_id}) created with permissions: {validated_permission_names}")
    return new_role

# --- Authentication & Authorization ---
def authenticate_user(email, password):
    """
    Authenticates a user by email and password.
    Returns the User object if successful, None otherwise.
    """
    # 1. Get user by email.
    # 2. If user exists and is active, verify password_hash against provided password.
    # 3. Return user object or None.

    if not email or not password:
        return None # Or raise ValueError for missing credentials

    user = _get_user_by_email_from_db(email)

    if not user:
        print(f"Authentication failed: User with email '{email}' not found.")
        return None

    if not user.get("is_active", False): # Default to False if is_active is missing for some reason
        print(f"Authentication failed: User '{email}' is not active.")
        return None

    if _verify_password(password, user.get("password_hash")):
        print(f"User '{email}' authenticated successfully.")
        # For safety, typically don't return password_hash with the authenticated user object.
        # For mock purposes, it's less critical, but good practice.
        user_to_return = user.copy()
        # del user_to_return["password_hash"] # Or don't delete for mock simplicity
        return user_to_return
    else:
        print(f"Authentication failed: Invalid password for user '{email}'.")
        return None

def check_user_permission(user_id, permission_name, resource_object=None):
    """
    Checks if a user has a specific permission, possibly for a specific resource.
    `resource_object` can be a Task, Client, etc., to check for ownership or specific conditions.
    """
    # 1. Get user and their role(s).
    # 2. Get the Permission object by permission_name.
    # 3. Check if the user's role(s) include this permission.
    # 4. If resource_object is provided, apply any resource-specific logic
    #    (e.g., is the user the owner of the task? Is the task within the user's client scope?).
    #    This part can be complex and might involve specific checks per resource type.
    # 5. Return True or False.
    # This needs to be tightly integrated with src/core/rbac_models.py and multi-tenancy.
    pass

# This file will grow significantly as features are implemented.
# It acts as an abstraction layer over the raw data models.
# Consider using classes for services if state or dependencies (like db session) need to be managed.
# e.g., class UserService: def __init__(self, db_session): self.db = db_session ...

# --- Mock Data Structures and Helper Functions ---

_MOCK_USER_DB = [] # List to store user dictionaries
_MOCK_ROLE_DB = [] # List to store role dictionaries
_MOCK_PERMISSION_DB = [ # Pre-populated with some example permission names
    "task.create", "task.edit.own", "task.edit.all", "task.delete",
    "client.view.all", "client.edit.assigned", "user.manage", "content.approve"
]
_NEXT_USER_ID = 1
_NEXT_ROLE_ID = 1

def _get_next_user_id():
    global _NEXT_USER_ID
    new_id = _NEXT_USER_ID
    _NEXT_USER_ID += 1
    return new_id

def _get_next_role_id():
    global _NEXT_ROLE_ID
    new_id = _NEXT_ROLE_ID
    _NEXT_ROLE_ID += 1
    return new_id

def _get_user_by_email_from_db(email):
    """Conceptual: Fetches a user by email from the mock database."""
    for user in _MOCK_USER_DB:
        if user['email'] == email:
            return user
    return None

def _get_user_by_id_from_db(user_id):
    """Conceptual: Fetches a user by ID from the mock database."""
    for user in _MOCK_USER_DB:
        if user['id'] == user_id:
            return user
    return None

def _save_user_to_db(user_object):
    """Conceptual: 'Saves' a user to the mock database (updates if exists, else appends)."""
    for i, user in enumerate(_MOCK_USER_DB):
        if user['id'] == user_object['id']:
            _MOCK_USER_DB[i] = user_object
            print(f"MockUserDB: User {user_object['id']} updated: {user_object}")
            return
    _MOCK_USER_DB.append(user_object)
    print(f"MockUserDB: User {user_object['id']} added: {user_object}")

def _get_role_by_name_from_db(name):
    """Conceptual: Fetches a role by name from the mock database."""
    for role in _MOCK_ROLE_DB:
        if role['name'] == name:
            return role
    return None

def _get_role_by_id_from_db(role_id):
    """Conceptual: Fetches a role by ID from the mock database."""
    for role in _MOCK_ROLE_DB:
        if role['id'] == role_id:
            return role
    return None

def _save_role_to_db(role_object):
    """Conceptual: 'Saves' a role to the mock database (updates if exists, else appends)."""
    for i, role in enumerate(_MOCK_ROLE_DB):
        if role['id'] == role_object['id']:
            _MOCK_ROLE_DB[i] = role_object
            print(f"MockRoleDB: Role {role_object['id']} updated: {role_object}")
            return
    _MOCK_ROLE_DB.append(role_object)
    print(f"MockRoleDB: Role {role_object['id']} added: {role_object}")

def _hash_password(password):
    """Mock password hashing."""
    if not password: return None
    return f"hashed_{password}"

def _verify_password(plain_password, hashed_password):
    """Mock password verification."""
    if not plain_password or not hashed_password: return False
    return hashed_password == f"hashed_{plain_password}"

def _check_user_permission(user_id, action, context_object=None):
    """
    Conceptual: Mock permission check for user services.
    For now, this is highly simplified and generally permissive.
    A real implementation would involve fetching user's role, then role's permissions.
    """
    print(f"MockUserAuth: Checking permission for user {user_id} to '{action}' with context {context_object}.")
    # Example: Only an admin (e.g., user_id 1 with a specific role) can manage roles.
    # if action == "manage_roles":
    #     user = _get_user_by_id_from_db(user_id)
    #     if user and _get_role_by_id_from_db(user.get('role_id')).get('name') == "Admin": # Highly conceptual
    #         return True
    #     return False
    return True # Default to allow for now
