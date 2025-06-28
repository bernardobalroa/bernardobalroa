# src/tasks/services.py
# Placeholder for task and project management business logic

"""
This service layer module will handle the business logic for tasks,
projects (if implemented as a separate entity), comments, and attachments.
It will interact with `src/tasks/models.py` and services like `user_services`
(for assignees, reporters) and `client_services` (for client-specific tasks).

Key Functions/Operations to be implemented:

Task Management:
- create_task(title, description, client_id=None, assignee_id=None, reporter_id, priority="Medium", due_date=None, status="To-Do", project_id=None, ...)
  - `reporter_id` is the ID of the user creating the task.
  - Validates that `assignee_id`, `client_id`, `project_id` are valid and accessible by the reporter.
  - Applies multi-tenancy: task is associated with `client_id` or is an internal agency task.
- get_task_by_id(task_id, requesting_user_context)
  - Enforces RBAC and multi-tenancy. Users should only see tasks they are allowed to access
    (e.g., assigned to them, for their client, or if they have broader permissions).
- update_task(task_id, requesting_user_context, title=None, description=None, status=None, priority=None, due_date=None, assignee_id=None, ...)
  - Requires appropriate permissions (e.g., only assignee or manager can update certain fields).
  - Handles status transitions (workflow logic, e.g., "In Progress" -> "In Review").
- delete_task(task_id, requesting_user_context)
  - Requires specific permission.
- list_tasks(requesting_user_context, filters=None, sort_by=None, pagination=None)
  - `filters` could include: client_id, assignee_id, status, priority, project_id, due_date_range.
  - This is fundamental for task lists, Kanban boards, and personalized dashboards.
  - "Role-Specific Views": Filtering will be key to tailoring views for Videographers, Editors, etc.

Task Workflow (Content Collaboration related - specific functions to be detailed below):
- Manages transitions of `content_status` (e.g., "RawUploaded", "PendingReview", "Approved").
- Handles notifications for content workflow steps (e.g., to reviewer when content is submitted).
- Integrates with permission checks (e.g., only assigned editor can submit for review).

Comments & Attachments:
- add_comment_to_task(task_id, user_id, text_content, requesting_user_context) # Added requesting_user_context
- list_comments_for_task(task_id, requesting_user_context)
- add_attachment_to_task(task_id, user_id, file_url=None, file_name=None, attachment_type="link") # Support direct uploads later
- list_attachments_for_task(task_id, requesting_user_context)

Project Management (if Project model is used):
- create_project(name, client_id, manager_id, description=None, ...)
- get_project_by_id(project_id, requesting_user_context)
- list_projects_for_client(client_id, requesting_user_context)
- add_task_to_project(task_id, project_id, requesting_user_context)

Notifications:
- Many actions here (task assignment, status change, new comment, approval request)
  should trigger notifications (in-app, email) to relevant users.
  This might involve a separate notification_service.

Important Considerations:
- Multi-Tenancy: Tasks for specific clients must be strictly isolated. Internal agency tasks
  might have a null `client_id` or a special agency `client_id`.
- RBAC: Permissions like "task.create", "task.edit.own", "task.edit.all",
  "task.change_status.approve", "task.assign" will be heavily used.
- Workflow Engine: For complex status transitions and automations, a more formal
  workflow engine might be considered later. For now, service logic can handle it.
- Performance: `list_tasks` needs to be efficient, especially with many filters.
  Database indexing will be critical.
- Atomicity: Operations like creating a task and sending a notification should be robust.
"""

# Placeholder function signatures

def create_task(reporter_id, title, description, client_id=None, assignee_id=None, **kwargs):
    """
    Creates a new task.
    `reporter_id` is the user creating the task.
    `kwargs` can include priority, due_date, status, project_id, content links etc.
    """
    # 1. Validate input. Check permissions of `reporter_id`.
    # 2. Ensure `client_id` (if provided) is valid and accessible by reporter.
    # 3. Ensure `assignee_id` (if provided) is valid.
    # 4. Create Task object and save to DB.
    #    - task = Task(reporter_id=reporter_id, title=title, ..., client_id=client_id, assignee_id=assignee_id)
    # 5. If `assignee_id` is set, notify the assignee.
    # 6. Log creation.
    # 7. Return Task object or task_id.

    # Conceptual Permission Check for the reporter
    if not _check_permission(reporter_id, "create_task", {"client_id": client_id}): # Pass client_id for context
        print(f"User {reporter_id} does not have permission to create tasks (potentially for client {client_id}).")
        raise PermissionError(f"User {reporter_id} cannot create tasks.")

    # Basic validation
    if not title:
        raise ValueError("Task title cannot be empty.")

    # Generate a new task ID (simple increment for mock)
    new_task_id = len(_MOCK_TASK_DB) + 1
    while any(t['id'] == new_task_id for t in _MOCK_TASK_DB): # Ensure uniqueness if tasks were deleted
        new_task_id +=1

    # Default values from Task model comments
    default_status = kwargs.get('status', "To-Do")
    default_priority = kwargs.get('priority', "Medium")
    default_content_status = kwargs.get('content_status', "NotStarted")
    default_content_version = kwargs.get('content_version', 0)

    new_task = {
        "id": new_task_id,
        "reporter_id": reporter_id,
        "title": title,
        "description": description,
        "client_id": client_id,
        "assignee_id": assignee_id,
        "status": default_status, # Overall task status
        "priority": default_priority,
        "due_date": kwargs.get('due_date', None),
        "project_id": kwargs.get('project_id', None),
        "reviewer_id": kwargs.get('reviewer_id', None), # For content tasks
        # Content workflow fields
        "content_status": default_content_status,
        "raw_content_link": kwargs.get('raw_content_link', None),
        "script_brief_link": kwargs.get('script_brief_link', None),
        "edited_content_link": kwargs.get('edited_content_link', None),
        "content_version": default_content_version,
        "last_feedback_summary": kwargs.get('last_feedback_summary', None),
        # "created_at": datetime.now() # Conceptual, would use real datetime
        # "updated_at": datetime.now()
    }

    # Add to our mock DB
    # _save_task_to_db will append if ID not found
    _save_task_to_db(new_task)

    # Conceptual Notification for assignment
    if assignee_id:
        _notify_user(
            assignee_id,
            f"You have been assigned a new task: '{title}' (ID: {new_task_id})."
        )

    print(f"Task {new_task_id} created: '{title}' by user {reporter_id}.")
    return new_task

def get_task_by_id(task_id, requesting_user_context):
    """
    Retrieves a task by its ID, respecting tenancy and permissions.
    """
    # 1. Fetch task from DB.
    # 2. Verify `requesting_user_context` has permission to view this task.
    #    - Is it their task? Is it for their client? Do they have global view rights?
    #    - Check against effective client_id from multi-tenancy context.
    # 3. If not found or access denied, raise error.

    # Assuming requesting_user_context is an object or dict containing user_id
    # current_user_id = requesting_user_context.get('user_id') # Example
    # For mock, let's assume requesting_user_context IS the user_id for simplicity if not an object
    current_user_id = requesting_user_context if isinstance(requesting_user_context, int) else requesting_user_context.get('user_id', 0)


    task = _get_task_from_db(task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")

    # Conceptual Permission Check:
    # This check would be more complex in reality, involving user roles, client associations, etc.
    # For mock: check if user is reporter, assignee, or reviewer as a basic check.
    # A more generic "view_task" permission would be checked against the user's roles.
    permission_context = {
        "task_id": task_id,
        "assignee_id": task.get("assignee_id"),
        "reporter_id": task.get("reporter_id"),
        "reviewer_id": task.get("reviewer_id"),
        "client_id": task.get("client_id")
        # In a real system, user's client_id(s) would also be part of requesting_user_context
    }
    if not _check_permission(current_user_id, "get_task", permission_context):
        # In a real app, this would raise a specific exception like PermissionDeniedError
        # or the _get_task_from_db might be scoped by user visibility already.
        print(f"User {current_user_id} does not have permission to view task {task_id}.")
        raise PermissionError(f"User {current_user_id} cannot view task {task_id}.")

    print(f"Task {task_id} retrieved by user {current_user_id}.")
    return task


def delete_task(task_id, requesting_user_context):
    """
    Deletes a task.
    Requires specific permission, often limited to task reporter or managers/admins.
    """
    current_user_id = requesting_user_context if isinstance(requesting_user_context, int) else requesting_user_context.get('user_id', 0)

    task = _get_task_from_db(task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found to delete.")

    # Conceptual Permission Check:
    # User needs 'delete_task' permission. This might be restricted to admins,
    # or perhaps the reporter of the task if it's in an early stage.
    if not _check_permission(current_user_id, "delete_task", task):
        print(f"User {current_user_id} does not have permission to delete task {task_id}.")
        raise PermissionError(f"User {current_user_id} cannot delete task {task_id}.")

    # Mock Deletion Logic: Remove from the list
    global _MOCK_TASK_DB
    _MOCK_TASK_DB = [t for t in _MOCK_TASK_DB if t['id'] != task_id]

    print(f"Task {task_id} deleted by user {current_user_id}.")
    # In a real system, you might also delete associated comments, attachments, etc.,
    # or handle them based on cascading rules or soft-delete policies.
    return True


def list_tasks(requesting_user_context, filters=None, sort_by=None, pagination=None):
    """
    Lists tasks based on user's permissions and provided filters.
    This is core to dashboards and task boards.
    """
    # 1. Determine base query scope based on `requesting_user_context` (multi-tenancy).
    #    - e.g., `query = Task.query.filter(Task.client_id == current_client_id)`
    #    - Or, if user is Videographer, `query = query.filter(Task.assignee_id == user.id, Task.type == 'filming')` (simplified example)
    # 2. Apply `filters` (status, priority, assignee, etc.).
    # 3. Apply `sort_by`.
    # 4. Apply `pagination`.
    # 5. Return list of Task objects.

    # For mock, let's assume requesting_user_context IS the user_id for simplicity if not an object
    current_user_id = requesting_user_context if isinstance(requesting_user_context, int) else requesting_user_context.get('user_id', 0)

    # Conceptual Permission/Scope Check:
    # In a real system, this would first determine what client_id(s) the user can access,
    # then filter tasks by that. For super-admins, it might be all tasks.
    # For now, our mock _check_permission for "list_tasks" will just allow,
    # and we'll apply filters directly to the whole _MOCK_TASK_DB for simplicity.
    # The `task_object` for _check_permission in list context might be a generic
    # indicator like `{"action_scope": "all"}` or `{"client_id": user_client_id}`.
    if not _check_permission(current_user_id, "list_tasks", {"filters_intended": filters}):
        print(f"User {current_user_id} does not have permission to list tasks with these filters.")
        raise PermissionError(f"User {current_user_id} cannot list tasks.")

    results = []
    # Deepcopy to avoid modifying the original mock tasks if we were to manipulate them here.
    # For simple filtering, it's not strictly necessary but good practice.
    # tasks_to_filter = [dict(t) for t in _MOCK_TASK_DB]
    tasks_to_filter = _MOCK_TASK_DB


    if filters:
        for task in tasks_to_filter:
            match = True
            for key, value in filters.items():
                if task.get(key) != value:
                    match = False
                    break
            if match:
                results.append(dict(task)) # Append a copy
    else:
        # No filters, return all (conceptually, all tasks visible to the user)
        results = [dict(t) for t in tasks_to_filter]

    # Conceptual: Sorting (would be complex for mock)
    # if sort_by:
    #     print(f"Conceptual: Sorting by {sort_by} would happen here.")
    #     # e.g., results.sort(key=lambda x: x.get(sort_by_field, default_sort_value), reverse=is_descending)

    # Conceptual: Pagination (would be complex for mock)
    # if pagination:
    #     print(f"Conceptual: Pagination ({pagination}) would be applied here.")
    #     # e.g., start = (page - 1) * per_page; end = start + per_page; results = results[start:end]

    print(f"User {current_user_id} listed tasks. Filters: {filters}. Found: {len(results)} tasks.")
    return results

def update_task_status(task_id, new_status, requesting_user_context):
    """
    Updates the status of a task, potentially triggering workflow actions.
    """
    # 1. Get task and check permissions for `requesting_user_context` to change status.
    # 2. Validate `new_status` and if the transition from old_status to new_status is valid.
    # 3. Update task status.
    # 4. Trigger notifications or other actions based on status change
    #    (e.g., if status becomes "Waiting for Approval", notify reviewer).
    #    If "Approved", may trigger AI transcription service call.

    # This is a general update placeholder; specific status changes like content workflow
    # are handled by more specific functions (approve_content, request_changes_on_content, etc.)
    # This function would handle changes to title, description, priority, due_date, assignee, etc.

    # For mock, let's assume requesting_user_context IS the user_id for simplicity if not an object
    current_user_id = requesting_user_context if isinstance(requesting_user_context, int) else requesting_user_context.get('user_id', 0)

    task = _get_task_from_db(task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")

    # Conceptual Permission Check:
    # User needs 'update_task' permission. Granular checks for specific fields might also apply.
    if not _check_permission(current_user_id, "update_task", task): # Pass the whole task for context
        print(f"User {current_user_id} does not have permission to update task {task_id}.")
        raise PermissionError(f"User {current_user_id} cannot update task {task_id}.")

    updated_fields = []
    original_assignee = task.get('assignee_id')

    # Iterate through kwargs to update fields.
    # Add comments about fields that should be handled by specific workflow functions.
    for key, value in kwargs.items():
        if key in task: # Only update existing keys, or be more flexible if schema can evolve
            if key == "id": # ID should not be updatable
                print(f"Warning: Attempt to update 'id' for task {task_id} was ignored.")
                continue
            if key == "content_status":
                print(f"Warning: 'content_status' for task {task_id} should ideally be updated via specific workflow functions (e.g., approve_content). Allowing for now in mock.")
            if key == "status" and value == "PendingReview": # Example of a status that implies a workflow
                 print(f"Warning: Changing 'status' to 'PendingReview' for task {task_id} might be better handled by 'submit_for_review'. Allowing for now in mock.")

            if task[key] != value:
                task[key] = value
                updated_fields.append(key)
        else:
            print(f"Warning: Key '{key}' not found in task {task_id} schema, update ignored.")

    if not updated_fields:
        print(f"No fields updated for task {task_id}.")
        return task # Or raise a specific "NoChangesMade" error/return different status

    # task["updated_at"] = datetime.now() # Conceptual
    _save_task_to_db(task)

    # Conceptual Notifications:
    if "assignee_id" in updated_fields and task.get('assignee_id') != original_assignee:
        if original_assignee:
             _notify_user(original_assignee, f"You have been unassigned from task '{task.get('title', task_id)}'.")
        if task.get('assignee_id'):
            _notify_user(task['assignee_id'], f"You have been assigned to task '{task.get('title', task_id)}'.")

    # Generic update notification (could be to reporter or other stakeholders)
    if updated_fields:
        _notify_user(task.get('reporter_id'), f"Task '{task.get('title', task_id)}' has been updated. Changed fields: {', '.join(updated_fields)}.")

    print(f"Task {task_id} updated by user {current_user_id}. Changed fields: {', '.join(updated_fields) if updated_fields else 'None'}.")
    return task

def add_comment_to_task(task_id, user_id, text_content, requesting_user_context):
    """
    Adds a comment to a task.
    """
    # 1. Get task, check if `requesting_user_context` (user_id) can comment on this task.
    # 2. Create Comment object and save.
    # 3. Notify relevant parties about the new comment.

    task = _get_task_from_db(task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")

    # Conceptual Permission Check:
    # User performing the action would be derived from `requesting_user_context` or `user_id`.
    if not _check_permission(user_id, "add_comment", {"task_id": task_id, "task_assignee_id": task.get("assignee_id"), "task_reporter_id": task.get("reporter_id")}):
        print(f"User {user_id} does not have permission to comment on task {task_id}.")
        raise PermissionError(f"User {user_id} cannot comment on task {task_id}.")

    if not text_content or not text_content.strip():
        raise ValueError("Comment text cannot be empty.")

    # Conceptual Comment Creation:
    # For now, we'll just print. A real implementation would create a Comment record.
    # A mock comment DB and _save_comment_to_db could be added later if needed for more complex testing.
    mock_comment_id = len(_MOCK_TASK_DB) + 1000 + len(task.get("comments", [])) # semi-unique ID for mock
    new_comment = {
        'id': mock_comment_id,
        'task_id': task_id,
        'user_id': user_id,
        'text_content': text_content,
        # 'created_at': datetime.now() # Conceptual
    }
    # Conceptually add to a list of comments on the task or a separate comment DB
    if "comments" not in task:
        task["comments"] = []
    task["comments"].append(new_comment)
    _save_task_to_db(task) # Re-save task if comments are embedded or to update an 'updated_at' field

    print(f"MockComment: User {user_id} added comment to task {task_id}: '{text_content}' (CommentID: {mock_comment_id})")

    # Conceptual Notifications:
    # Notify assignee if they aren't the one commenting
    if task.get('assignee_id') and task.get('assignee_id') != user_id:
        _notify_user(
            task['assignee_id'],
            f"New comment on task '{task.get('title', task_id)}' by user {user_id}: '{text_content}'"
        )
    # Notify reporter if they aren't the one commenting and also not the assignee
    if task.get('reporter_id') and task.get('reporter_id') != user_id and task.get('reporter_id') != task.get('assignee_id'):
        _notify_user(
            task['reporter_id'],
            f"New comment on task '{task.get('title', task_id)}' (that you reported) by user {user_id}: '{text_content}'"
        )

    return new_comment # Return the conceptual comment object


def list_comments_for_task(task_id, requesting_user_context):
    """
    Lists all comments for a given task.
    Requires permission to view the task itself.
    """
    current_user_id = requesting_user_context if isinstance(requesting_user_context, int) else requesting_user_context.get('user_id', 0)

    task = _get_task_from_db(task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")

    # Conceptual Permission Check:
    # If user can 'get_task', they can probably list its comments.
    # Or a more specific 'list_comments' permission could be used.
    permission_context = {
        "task_id": task_id,
        "assignee_id": task.get("assignee_id"),
        "reporter_id": task.get("reporter_id"),
        "reviewer_id": task.get("reviewer_id"),
        "client_id": task.get("client_id")
    }
    if not _check_permission(current_user_id, "list_comments", permission_context): # Using "list_comments" or could reuse "get_task"
        print(f"User {current_user_id} does not have permission to list comments for task {task_id}.")
        raise PermissionError(f"User {current_user_id} cannot list comments for task {task_id}.")

    comments = task.get("comments", [])
    print(f"User {current_user_id} listed {len(comments)} comments for task {task_id}.")
    return comments


def add_attachment_to_task(task_id, user_id, file_url, file_name=None, attachment_type="link", requesting_user_context=None):
    """
    Adds an attachment (file link) to a task.
    """
    current_user_id = user_id # Assuming user_id is passed directly for who is adding.
                              # requesting_user_context could be used for more complex auth.

    task = _get_task_from_db(task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")

    if not _check_permission(current_user_id, "add_attachment", {"task_id": task_id}):
        print(f"User {current_user_id} does not have permission to add attachments to task {task_id}.")
        raise PermissionError(f"User {current_user_id} cannot add attachments to task {task_id}.")

    if not file_url or not file_url.strip():
        raise ValueError("File URL must be provided for attachment.")

    mock_attachment_id = len(_MOCK_TASK_DB) + 2000 + len(task.get("attachments", [])) # semi-unique ID
    new_attachment = {
        'id': mock_attachment_id,
        'task_id': task_id,
        'user_id': current_user_id, # User who added the attachment
        'file_url': file_url,
        'file_name': file_name if file_name else file_url.split('/')[-1], # Basic name extraction
        'attachment_type': attachment_type,
        # 'uploaded_at': datetime.now() # Conceptual
    }

    if "attachments" not in task:
        task["attachments"] = []
    task["attachments"].append(new_attachment)
    _save_task_to_db(task)

    print(f"MockAttachment: User {current_user_id} added attachment to task {task_id}: '{new_attachment['file_name']}' (URL: {file_url})")

    # Conceptual Notification (e.g., to task assignee or reporter)
    # _notify_user(task.get('assignee_id'), f"New attachment '{new_attachment['file_name']}' added to task '{task.get('title', task_id)}'.")

    return new_attachment


def list_attachments_for_task(task_id, requesting_user_context):
    """
    Lists all attachments for a given task.
    Requires permission to view the task itself.
    """
    current_user_id = requesting_user_context if isinstance(requesting_user_context, int) else requesting_user_context.get('user_id', 0)

    task = _get_task_from_db(task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")

    # Conceptual Permission Check:
    # Similar to list_comments, if user can 'get_task', they can probably list its attachments.
    permission_context = {
        "task_id": task_id,
        "client_id": task.get("client_id")
        # Add other relevant context if needed for permission decisions
    }
    if not _check_permission(current_user_id, "list_attachments", permission_context): # Using "list_attachments" or could reuse "get_task"
        print(f"User {current_user_id} does not have permission to list attachments for task {task_id}.")
        raise PermissionError(f"User {current_user_id} cannot list attachments for task {task_id}.")

    attachments = task.get("attachments", [])
    print(f"User {current_user_id} listed {len(attachments)} attachments for task {task_id}.")
    return attachments


# This service maps to "Internal Task Management Module" and parts of "Content Collaboration & Workflow".
# It will be one of the most complex services in Phase 1.

# --- Content Workflow Specific Functions (Refactored for ContentAsset) ---

def create_content_asset(task_id, user_id, asset_type, name=None, raw_content_link=None, source_document_link=None, assignee_id=None, reviewer_id=None, requesting_user_context=None):
    """
    Creates a new content asset associated with a task.
    Typically called when initiating a new piece of content for a task.
    """
    # 1. Fetch parent task to ensure it exists.
    # 2. Permission check: Can user_id create content assets for this task_id?
    # 3. Create ContentAsset object with initial values (e.g., content_status="NotStarted", version=1).
    # 4. Save ContentAsset object (to _MOCK_CONTENT_ASSET_DB).
    # 5. Return new ContentAsset object.
    # This function now takes over some responsibility from the old upload_raw_content,
    # focusing on creating the asset record. Uploading links might be a subsequent update to this asset.

    current_user_id = user_id # Assuming user_id is authoritative for creation context for now.
                              # requesting_user_context might be used for more complex permission logic.

    # 1. Fetch parent task to ensure it exists.
    parent_task = _get_task_from_db(task_id)
    if not parent_task:
        raise ValueError(f"Parent task with ID {task_id} not found. Cannot create content asset.")

    # 2. Permission check: Can user_id create content assets for this task_id?
    # Pass task object for context if needed by permission check
    if not _check_permission(current_user_id, "create_content_asset", {"task_id": task_id, "task_client_id": parent_task.get("client_id")}):
        print(f"User {current_user_id} does not have permission to create content assets for task {task_id}.")
        raise PermissionError(f"User {current_user_id} cannot create content assets for task {task_id}.")

    if not asset_type or not asset_type.strip():
        raise ValueError("asset_type must be provided.")

    # 3. Create ContentAsset object with initial values
    new_asset_id = _get_next_content_asset_id()
    new_asset = {
        "id": new_asset_id,
        "task_id": task_id,
        "name": name,
        "asset_type": asset_type,
        "content_status": "NotStarted", # Default status
        "version_number": 1, # Initial version
        "raw_content_link": raw_content_link,
        "source_document_link": source_document_link,
        "current_content_link": None, # Typically set when first version is ready or submitted
        "published_url": None,
        "assignee_id": assignee_id, # Specific assignee for this asset
        "reviewer_id": reviewer_id, # Specific reviewer for this asset
        "last_feedback_summary": None,
        # "created_at": datetime.now(), # Conceptual
        # "updated_at": datetime.now()  # Conceptual
    }

    # 4. Save ContentAsset object (to _MOCK_CONTENT_ASSET_DB).
    _save_content_asset_to_db(new_asset)

    # Conceptual Notification (e.g., to asset assignee if provided)
    if new_asset.get('assignee_id'):
        _notify_user(
            new_asset['assignee_id'],
            f"You have been assigned a new content asset: '{new_asset.get('name', asset_type)}' (ID: {new_asset_id}) for task '{parent_task.get('title', task_id)}'."
        )

    print(f"ContentAsset (ID: {new_asset_id}, Type: {asset_type}, Name: {name}) created for task {task_id} by user {current_user_id}.")
    # 5. Return new ContentAsset object.
    return new_asset

def update_content_asset_links(content_asset_id, user_id, raw_link=None, source_document_link=None, edited_link=None, requesting_user_context=None):
    """
    Updates links for a specific content asset. Could set content_status to 'RawUploaded' or 'EditingInProgress'.
    """
    # 1. Fetch ContentAsset by content_asset_id.
    # 2. Permission check.
    # 3. Update link fields.
    # 4. Update content_status (e.g., to "RawUploaded" if raw_link is provided).
    # 5. Increment version if it's a new version of raw/edited content.
    # 6. Save ContentAsset.
    # 7. Notify relevant parties (e.g., assigned editor if raw content uploaded).
    print(f"Conceptual: update_content_asset_links for asset {content_asset_id}")
    pass


def submit_content_asset_for_review(content_asset_id, user_id, edited_content_link, requesting_user_context=None):
    """
    Submits a specific content asset for review.
    Updates the asset's status to "PendingReview" and notifies its designated reviewer.
    Args:
        content_asset_id (int): The ID of the content asset.
        user_id (int): The ID of the user submitting for review (e.g., an Editor).
        edited_content_link (str): URL to the edited content for this asset.
    """
    # 1. Fetch ContentAsset by content_asset_id.
    # 2. Permission check (e.g., user_id is assignee of the ContentAsset).
    # 3. Ensure ContentAsset has a reviewer_id.
    # 4. Update ContentAsset's current_content_link = edited_content_link.
    # 5. Set ContentAsset's content_status = "PendingReview".
    # 6. Save ContentAsset.
    # 7. Notify the ContentAsset's reviewer_id.
    print(f"Conceptual: submit_content_asset_for_review for asset {content_asset_id}")
    # Old logic for task:
    # task = _get_task_from_db(task_id) ...
    # task['edited_content_link'] = edited_content_link
    # task['content_status'] = "PendingReview" ...
    # _notify_user(task['reviewer_id'], ...)

    current_user_id = user_id # User performing the submission

    asset = _get_content_asset_from_db(content_asset_id)
    if not asset:
        raise ValueError(f"ContentAsset with ID {content_asset_id} not found.")

    # Permission Check: e.g., current_user_id should be asset['assignee_id']
    permission_context = {"content_asset_id": content_asset_id, "asset_assignee_id": asset.get("assignee_id")}
    if not _check_permission(current_user_id, "submit_content_asset_for_review", permission_context):
        print(f"User {current_user_id} does not have permission to submit content asset {content_asset_id} for review.")
        raise PermissionError(f"User {current_user_id} cannot submit content asset {content_asset_id} for review.")

    if not asset.get("reviewer_id"):
        raise ValueError(f"ContentAsset {content_asset_id} does not have a designated reviewer_id. Cannot submit for review.")

    if not edited_content_link or not edited_content_link.strip():
        raise ValueError("edited_content_link must be provided when submitting for review.")

    asset['current_content_link'] = edited_content_link
    asset['content_status'] = "PendingReview"
    # asset['submitted_for_review_at'] = datetime.now() # Conceptual
    # Versioning: Decide if submitting for review automatically increments version.
    # For now, let's assume version was incremented when the edited_content_link was last updated
    # via update_content_asset_links or during creation if provided then.
    # If a new version is explicitly created upon *each* submission, then:
    # asset['version_number'] = (asset.get('version_number', 0) or 0) + 1


    _save_content_asset_to_db(asset)

    parent_task = _get_task_from_db(asset.get("task_id"))
    task_title = parent_task.get("title", asset.get("task_id")) if parent_task else asset.get("task_id")


    _notify_user(
        asset['reviewer_id'],
        f"Content asset '{asset.get('name', content_asset_id)}' (Version {asset.get('version_number', 'N/A')}) for task '{task_title}' is ready for your review. Link: {asset['current_content_link']}"
    )

    print(f"ContentAsset {content_asset_id} submitted for review by user {current_user_id}. Status: PendingReview")
    return asset

def approve_content_asset(content_asset_id, reviewer_id, requesting_user_context=None):
    """
    Approves a specific content asset.
    Sets the asset's content_status to "Approved".
    Args:
        content_asset_id (int): The ID of the content asset.
        reviewer_id (int): The ID of the user approving (must match asset's reviewer_id).
    """
    # 1. Fetch ContentAsset by content_asset_id.
    # 2. Permission check (reviewer_id matches ContentAsset.reviewer_id).
    # 3. Ensure ContentAsset.content_status is "PendingReview".
    # 4. Set ContentAsset.content_status = "Approved".
    # 5. Save ContentAsset.
    # 6. Notify relevant parties (asset assignee, task reporter, etc.).
    # 7. Conceptual: Trigger AI transcription for this asset's approved link.

    current_user_id = reviewer_id # The user performing the approval IS the reviewer_id for this function

    asset = _get_content_asset_from_db(content_asset_id)
    if not asset:
        raise ValueError(f"ContentAsset with ID {content_asset_id} not found.")

    # Permission Check: current_user_id must be the asset['reviewer_id']
    if asset.get("reviewer_id") != current_user_id:
        print(f"User {current_user_id} is not the designated reviewer for content asset {content_asset_id} (actual: {asset.get('reviewer_id')}).")
        raise PermissionError(f"User {current_user_id} is not the designated reviewer for content asset {content_asset_id}.")

    if not _check_permission(current_user_id, "approve_content_asset", {"content_asset_id": content_asset_id, "asset_reviewer_id": asset.get("reviewer_id")}):
        print(f"User {current_user_id} does not have permission to approve content asset {content_asset_id}.")
        raise PermissionError(f"User {current_user_id} cannot approve content asset {content_asset_id}.")

    if asset.get("content_status") != "PendingReview":
        raise ValueError(f"ContentAsset {content_asset_id} is in status '{asset.get('content_status')}', cannot approve. Expected 'PendingReview'.")

    asset['content_status'] = "Approved"
    # asset['approved_at'] = datetime.now() # Conceptual

    _save_content_asset_to_db(asset)

    parent_task = _get_task_from_db(asset.get("task_id"))
    task_title = parent_task.get("title", asset.get("task_id")) if parent_task else asset.get("task_id")

    # Conceptual Notifications:
    # Notify asset assignee
    if asset.get('assignee_id') and asset.get('assignee_id') != current_user_id:
        _notify_user(
            asset['assignee_id'],
            f"Your submitted content asset '{asset.get('name', content_asset_id)}' for task '{task_title}' has been approved."
        )
    # Notify parent task's reporter (if different from current user and asset assignee)
    if parent_task and parent_task.get('reporter_id') and \
       parent_task.get('reporter_id') != current_user_id and \
       parent_task.get('reporter_id') != asset.get('assignee_id'):
        _notify_user(
            parent_task['reporter_id'],
            f"Content asset '{asset.get('name', content_asset_id)}' for task '{task_title}' has been approved by user {current_user_id}."
        )

    print(f"ContentAsset {content_asset_id} approved by user {current_user_id}. Status: Approved.")

    # Placeholder for Phase 4: AI Transcription
    print(f"Conceptual: Trigger AI transcription for asset {content_asset_id}, link: {asset.get('current_content_link')}")
    # if asset.get('current_content_link'):
    #    ai_service.trigger_transcription(asset['current_content_link'], content_asset_id)

    return asset

def request_changes_on_content_asset(content_asset_id, reviewer_id, feedback_comment_text, requesting_user_context=None):
    """
    Requests changes on a specific content asset.
    Sets the asset's content_status to "ChangesRequested" and adds feedback.
    Args:
        content_asset_id (int): The ID of the content asset.
        reviewer_id (int): The ID of the user requesting changes.
        feedback_comment_text (str): The feedback.
    """
    # 1. Fetch ContentAsset by content_asset_id.
    # 2. Permission check (reviewer_id matches ContentAsset.reviewer_id).
    # 3. Ensure ContentAsset.content_status is "PendingReview".
    # 4. Set ContentAsset.content_status = "ChangesRequested".
    # 5. Update ContentAsset.last_feedback_summary.
    # 6. Conceptually add feedback_comment_text as a comment linked to the ContentAsset (or Task).
    #    (This might need a new add_comment_to_content_asset function or refinement of add_comment_to_task)
    # 7. Save ContentAsset.
    # 8. Notify the ContentAsset's assignee.

    current_user_id = reviewer_id # The user performing the action IS the reviewer_id

    asset = _get_content_asset_from_db(content_asset_id)
    if not asset:
        raise ValueError(f"ContentAsset with ID {content_asset_id} not found.")

    # Permission Check: current_user_id must be the asset['reviewer_id']
    if asset.get("reviewer_id") != current_user_id:
        print(f"User {current_user_id} is not the designated reviewer for content asset {content_asset_id} (actual: {asset.get('reviewer_id')}).")
        raise PermissionError(f"User {current_user_id} is not the designated reviewer for content asset {content_asset_id}.")

    if not _check_permission(current_user_id, "request_changes_on_content_asset", {"content_asset_id": content_asset_id, "asset_reviewer_id": asset.get("reviewer_id")}):
        print(f"User {current_user_id} does not have permission to request changes for content asset {content_asset_id}.")
        raise PermissionError(f"User {current_user_id} cannot request changes for content asset {content_asset_id}.")

    if asset.get("content_status") != "PendingReview":
        raise ValueError(f"ContentAsset {content_asset_id} is in status '{asset.get('content_status')}', cannot request changes. Expected 'PendingReview'.")

    if not feedback_comment_text or not feedback_comment_text.strip():
        raise ValueError("Feedback comment text must be provided when requesting changes.")

    asset['content_status'] = "ChangesRequested"
    asset['last_feedback_summary'] = feedback_comment_text[:255] # Store a summary
    # asset['current_content_link'] = None # Optionally clear the current_content_link, or leave as is for reference
    # asset['version_number'] = (asset.get('version_number', 0) or 0) + 1 # Increment version for the next iteration

    # Conceptually add the full feedback as a comment.
    # This would ideally link to the ContentAsset itself if comments can be per-asset,
    # or fall back to task-level comments if that's the model.
    parent_task_id = asset.get("task_id")
    print(f"Conceptual: Calling add_comment_to_task(task_id={parent_task_id}, user_id={current_user_id}, text='Feedback on asset {content_asset_id} ({asset.get('name')}): {feedback_comment_text}')")
    # add_comment_to_task(parent_task_id, current_user_id, f"Feedback on asset {asset.get('name', content_asset_id)}: {feedback_comment_text}", requesting_user_context)

    _save_content_asset_to_db(asset)

    # Conceptual Notification to the asset's assignee
    if asset.get('assignee_id'):
        parent_task = _get_task_from_db(parent_task_id)
        task_title = parent_task.get("title", parent_task_id) if parent_task else parent_task_id
        _notify_user(
            asset['assignee_id'],
            f"Changes have been requested by user {current_user_id} for content asset '{asset.get('name', content_asset_id)}' on task '{task_title}'. Feedback: {feedback_comment_text}"
        )

    print(f"Changes requested for content asset {content_asset_id} by user {current_user_id}. Status: ChangesRequested.")
    return asset

# Note: The original upload_raw_content, submit_for_review, approve_content,
# and request_changes_on_content functions that operated directly on Task fields
# are now superseded by the ContentAsset-focused versions above.
# They can be removed or heavily refactored if a Task can also have a *single* primary content flow
# in addition to multiple ContentAssets. For now, assume all content flows via ContentAssets.

# Note: `requesting_user_context` is added to these functions for consistency,
# allowing a central place (e.g., a decorator or middleware) to extract user_id
# and perform initial permission/tenancy checks if desired, rather than passing user_id separately.
# The actual implementation will depend on the chosen web framework and authentication system.

# --- Mock/Conceptual Helper Functions (for illustration purposes) ---

_MOCK_CONTENT_ASSET_DB = [
    {
        "id": 1, "task_id": 1, "name": "Alpha Video - Draft 1", "asset_type": "video",
        "content_status": "EditingInProgress", "version_number": 1,
        "raw_content_link": "http://example.com/raw/alpha_v1",
        "source_document_link": "http://example.com/script/alpha",
        "current_content_link": "http://example.com/edit/alpha_v1_draft1",
        "published_url": None,
        "assignee_id": 101, "reviewer_id": 102, "last_feedback_summary": None
    },
    {
        "id": 2, "task_id": 1, "name": "Alpha Video - Script", "asset_type": "script",
        "content_status": "Approved", "version_number": 1,
        "raw_content_link": None,
        "source_document_link": None,
        "current_content_link": "http://example.com/script/alpha_final",
        "published_url": None,
        "assignee_id": 201, "reviewer_id": 102, "last_feedback_summary": None
    },
    {
        "id": 3, "task_id": 3, "name": "Gamma Presentation - Review Copy", "asset_type": "presentation",
        "content_status": "PendingReview", "version_number": 2,
        "raw_content_link": "http://example.com/raw/gamma_v2",
        "source_document_link": "http://example.com/brief/gamma",
        "current_content_link": "http://example.com/edit/gamma_v2_review",
        "published_url": None,
        "assignee_id": 101, "reviewer_id": 102, "last_feedback_summary": "Needs more pizzazz on slide 5."
    }
]
_NEXT_CONTENT_ASSET_ID = 4 # Start next ID after the manually added ones

def _get_next_content_asset_id():
    global _NEXT_CONTENT_ASSET_ID
    new_id = _NEXT_CONTENT_ASSET_ID
    _NEXT_CONTENT_ASSET_ID += 1
    return new_id

def _get_content_asset_from_db(asset_id):
    """Conceptual: Fetches a content asset by ID from the mock database."""
    for asset in _MOCK_CONTENT_ASSET_DB:
        if asset['id'] == asset_id:
            return asset
    return None

def _save_content_asset_to_db(asset_object):
    """Conceptual: 'Saves' a content asset to the mock database (updates if exists, else appends)."""
    for i, asset in enumerate(_MOCK_CONTENT_ASSET_DB):
        if asset['id'] == asset_object['id']:
            _MOCK_CONTENT_ASSET_DB[i] = asset_object
            print(f"MockContentAssetDB: Asset {asset_object['id']} updated: {asset_object}")
            return
    _MOCK_CONTENT_ASSET_DB.append(asset_object)
    print(f"MockContentAssetDB: Asset {asset_object['id']} added: {asset_object}")


# In a real application, these would be replaced by actual database interactions,
# authentication/authorization services, and notification systems.

# Conceptual database (in-memory list for mocking)
# Note: Direct content fields (content_status, raw_content_link, etc.) are removed from tasks.
# These are now managed in _MOCK_CONTENT_ASSET_DB, linked by task_id.
_MOCK_TASK_DB = [
    {"id": 1, "title": "Video Project Alpha", "client_id": 10, "assignee_id": 101, "reporter_id": 201, "status": "In Progress", "priority": "High", "comments": [], "attachments": []}, # reviewer_id removed from task, now per-asset
    {"id": 2, "title": "Blog Post Beta", "client_id": 20, "assignee_id": 103, "reporter_id": 202, "status": "To-Do", "priority": "Medium", "comments": [], "attachments": []},
    {"id": 3, "title": "Client Presentation Gamma", "client_id": 10, "assignee_id": 101, "reporter_id": 201, "status": "In Progress", "priority": "High", "comments": [], "attachments": []},
    {"id": 4, "title": "Internal KB Update", "client_id": None, "assignee_id": 102, "reporter_id": 201, "status": "To-Do", "priority": "Low", "comments": [], "attachments": []}, # No content workflow applicable here
]

def _get_task_from_db(task_id):
    """Conceptual: Fetches a task from the mock database."""
    for task in _MOCK_TASK_DB:
        if task['id'] == task_id:
            return task # Return a copy to avoid modifying the mock DB directly by reference in some cases
    return None

def _save_task_to_db(task_object):
    """Conceptual: 'Saves' a task to the mock database."""
    for i, task in enumerate(_MOCK_TASK_DB):
        if task['id'] == task_object['id']:
            _MOCK_TASK_DB[i] = task_object
            print(f"MockDB: Task {task_object['id']} updated: {task_object}")
            return
    # If not found, add it (for conceptual create_task if it were here)
    _MOCK_TASK_DB.append(task_object)
    print(f"MockDB: Task {task_object['id']} added: {task_object}")


def _check_permission(user_id, action, task_object):
    """
    Conceptual: Checks if a user has permission to perform an action on a task.
    For now, this is a very basic mock.
    A real implementation would involve checking user roles and permissions (RBAC).
    """
    print(f"MockAuth: Checking permission for user {user_id} to '{action}' on task {task_object.get('id', 'Unknown')}.")
    # Allow all actions for now for simplicity of service function flow
    # In reality, this would check:
    # - Is the user the assignee?
    # - Is the user a manager for the client associated with the task?
    # - Does the user's role (e.g., Videographer, Editor) grant this permission?
    if action == "upload_raw_content":
        # Example: Maybe only an assignee or a user with a 'Videographer' role can upload.
        # For this mock, let's say user 1 (Videographer role) or task assignee can upload.
        # if user_id == 1 or (task_object and task_object.get('assignee_id') == user_id):
        #     return True
        # Simplified for now, allowing the action.
        return True
    elif action == "submit_for_review":
        # Example: Only the current assignee (presumed Editor) can submit for review.
        # A real check:
        # if task_object and task_object.get('assignee_id') == user_id:
        #    return True
        # return False
        print(f"MockAuth: Allowing 'submit_for_review' for user {user_id} on task {task_object.get('id', 'Unknown')}.")
        return True # Simplified for now
    elif action in ["approve_content", "request_changes_on_content"]:
        # Example: Only the designated reviewer_id for the task can perform these actions.
        # A real check:
        # if task_object and task_object.get('reviewer_id') == user_id:
        #     return True
        # return False
        # For the mock, we also check if the user_id passed to _check_permission
        # matches the task's reviewer_id, as the service functions already do this.
        # So, this part of mock _check_permission is more about acknowledging the action string.
        if task_object and task_object.get('reviewer_id') == user_id:
             print(f"MockAuth: User {user_id} IS the designated reviewer for task {task_object.get('id')}. Allowing '{action}'.")
             return True
        # If the service function didn't pre-check, this mock would be more critical.
        # For now, just acknowledging the action is enough if the above condition isn't met explicitly.
        print(f"MockAuth: Allowing '{action}' for user {user_id} on task {task_object.get('id', 'Unknown')} (default for reviewer actions).")
        return True # Simplified for now, assuming service function does primary check of user vs task.reviewer_id.
    elif action == "create_task":
        # Example: Any authenticated user might be able to create a task.
        # More complex logic could check if they can create tasks for a specific client_id (passed in task_object for context here).
        print(f"MockAuth: Allowing 'create_task' for user {user_id}.")
        return True
    elif action == "add_comment":
        # Example: Users involved in the task (reporter, assignee, reviewer) or with general comment perms can comment.
        # task_object here might contain task_id, task_assignee_id, task_reporter_id for context.
        print(f"MockAuth: Allowing 'add_comment' for user {user_id} on task {task_object.get('task_id', 'Unknown')}.")
        return True
    elif action == "get_task":
        # Example: User might need to be reporter, assignee, reviewer, or related to the client_id.
        # task_object here is the permission_context from get_task_by_id.
        # A real check would be complex, involving user's client associations.
        print(f"MockAuth: Allowing 'get_task' for user {user_id} on task {task_object.get('task_id', 'Unknown')}.")
        return True
    elif action == "update_task":
        # Example: User might need to be assignee, reporter, or manager.
        # task_object is the task itself.
        print(f"MockAuth: Allowing 'update_task' for user {user_id} on task {task_object.get('id', 'Unknown')}.")
        return True
    elif action == "list_tasks":
        # Example: All authenticated users can list tasks, but the list will be pre-filtered by their client access.
        # task_object here is `{"filters_intended": filters}`.
        print(f"MockAuth: Allowing 'list_tasks' for user {user_id}.")
        return True
    elif action == "delete_task":
        # Example: User might need to be reporter or manager/admin.
        # task_object is the task itself.
        print(f"MockAuth: Allowing 'delete_task' for user {user_id} on task {task_object.get('id', 'Unknown')}.")
        return True
    elif action == "list_comments": # Could reuse 'get_task' permission logic
        # task_object is permission_context from list_comments_for_task
        print(f"MockAuth: Allowing 'list_comments' for user {user_id} on task {task_object.get('task_id', 'Unknown')}.")
        return True
    elif action == "add_attachment":
        # task_object is {"task_id": task_id}
        print(f"MockAuth: Allowing 'add_attachment' for user {user_id} on task {task_object.get('task_id', 'Unknown')}.")
        return True
    elif action == "list_attachments": # Could reuse 'get_task' permission logic
        # task_object is permission_context from list_attachments_for_task
        print(f"MockAuth: Allowing 'list_attachments' for user {user_id} on task {task_object.get('task_id', 'Unknown')}.")
        return True
    elif action == "create_content_asset":
        # task_object is {"task_id": task_id, "task_client_id": parent_task.get("client_id")}
        # Example: User might need to be related to the task or have specific content creation role.
        print(f"MockAuth: Allowing 'create_content_asset' for user {user_id} for task {task_object.get('task_id', 'Unknown')}.")
        return True
    elif action == "update_content_asset":
        # task_object is {"content_asset_id": content_asset_id, "task_id": asset.get("task_id"), "asset_assignee_id": asset.get("assignee_id") }
        # Example: User might need to be the asset's assignee or task manager.
        print(f"MockAuth: Allowing 'update_content_asset' for user {user_id} on asset {task_object.get('content_asset_id', 'Unknown')}.")
        return True
    elif action == "submit_content_asset_for_review":
        # task_object is {"content_asset_id": id, "asset_assignee_id": asset.get("assignee_id")}
        # Example: Only asset's assignee can submit.
        if task_object and task_object.get('asset_assignee_id') == user_id:
            print(f"MockAuth: User {user_id} IS the assignee for asset {task_object.get('content_asset_id')}. Allowing '{action}'.")
            return True
        # Simplified for mock - allow if no specific assignee check, or make it stricter
        print(f"MockAuth: Allowing '{action}' for user {user_id} on asset {task_object.get('content_asset_id', 'Unknown')}.")
        return True
    elif action == "approve_content_asset":
        # task_object is {"content_asset_id": id, "asset_reviewer_id": asset.get("reviewer_id")}
        # Example: Only asset's reviewer can approve.
        if task_object and task_object.get('asset_reviewer_id') == user_id:
            print(f"MockAuth: User {user_id} IS the reviewer for asset {task_object.get('content_asset_id')}. Allowing '{action}'.")
            return True
        print(f"MockAuth: Allowing '{action}' for user {user_id} on asset {task_object.get('content_asset_id', 'Unknown')}.")
        return True
    elif action == "request_changes_on_content_asset":
        # task_object is {"content_asset_id": id, "asset_reviewer_id": asset.get("reviewer_id")}
        # Example: Only asset's reviewer can request changes.
        if task_object and task_object.get('asset_reviewer_id') == user_id:
            print(f"MockAuth: User {user_id} IS the reviewer for asset {task_object.get('content_asset_id')}. Allowing '{action}'.")
            return True
        print(f"MockAuth: Allowing '{action}' for user {user_id} on asset {task_object.get('content_asset_id', 'Unknown')}.")
        return True

    print(f"MockAuth: Defaulting to TRUE for action '{action}' for user {user_id} on context {task_object if task_object else 'N/A'}.") # Generalised context object name
    return True # Default to allow for other actions in mock


def _notify_user(user_id, message):
    """Conceptual: Sends a notification to a user."""
    # In a real app, this would use an email service, WebSocket, or other notification mechanism.
    print(f"MockNotify: Sending notification to user {user_id}: '{message}'")

pass
