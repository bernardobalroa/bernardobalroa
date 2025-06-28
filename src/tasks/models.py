# src/tasks/models.py
# Placeholder for task data model
# Assuming a Python/Django-like ORM structure for now

class Task:
    """
    Represents a task within the project management module.
    """
    # id: int (Primary Key)
    # title: str
    # description: str (Text, can be Markdown or rich text)
    # status: str (Overall task status, e.g., "To-Do", "In Progress", "Blocked", "Done")
    # priority: str (e.g., "Low", "Medium", "High", "Urgent")
    # due_date: date (Optional)
    # created_at: datetime
    # updated_at: datetime
    #
    # # Relationships
    # client_id: int (Foreign Key to Client model, Nullable) - Associates task with a specific client project.
    #                                                        - Null for internal agency tasks.
    # assignee_id: int (Foreign Key to User model, Nullable) - User responsible for the current phase of the task.
    # reporter_id: int (Foreign Key to User model) - User who created or reported the task.
    # project_id: int (Foreign Key to Project model, Nullable) - If tasks are grouped into larger projects.
    # reviewer_id: int (Foreign Key to User model, Nullable) - User designated to review/approve the content.
    #
    # # Content Workflow Specific Fields
    # # This section details fields specifically for tasks that involve a content creation/approval lifecycle.
    # content_status: str (Optional, e.g., "NotStarted", "RawUploaded", "EditingInProgress", "PendingReview", "ChangesRequested", "Approved")
    #   - This status is specific to the content lifecycle within the task.
    #   - It can work alongside the overall task `status`. For example, a task `status` could be "In Progress"
    #     while `content_status` moves from "RawUploaded" to "EditingInProgress".
    # raw_content_link: str (Optional, URL to raw footage/assets, e.g., Google Drive link)
    # script_brief_link: str (Optional, URL to script, brief, or supporting documents)
    # edited_content_link: str (Optional, URL to the edited version of the content ready for review)
    # content_version: int (Optional, simple version counter, e.g., 1, 2, for revisions)
    # last_feedback_summary: str (Optional, stores key feedback points from the last review cycle)
    #
    # # Note on version_history:
    # # A more complex `version_history` (e.g., JSON field or a separate ContentVersion model)
    # # could store an array of objects, each with {version, link, submitted_at, reviewer_feedback, reviewed_at}.
    # # For MVP, `content_version` and `last_feedback_summary` along with task comments might suffice.
    #
    # # Attachments & Comments (likely separate models with Many-to-One relationship to Task)
    # # attachments: list[Attachment] # General task attachments
    # # comments: list[Comment]
    pass

class Project: # Optional, if tasks need to be grouped beyond client association
    """
    Represents a larger project that can contain multiple tasks.
    """
    # id: int (Primary Key)
    # name: str
    # description: str (Optional)
    # client_id: int (Foreign Key to Client model)
    # manager_id: int (Foreign Key to User model, person overseeing the project)
    # start_date: date (Optional)
    # end_date: date (Optional)
    # status: str (e.g., "Planning", "Active", "Completed", "On Hold")
    # created_at: datetime
    # updated_at: datetime
    pass

class Comment:
    """
    Represents a comment made on a task.
    """
    # id: int (Primary Key)
    # task_id: int (Foreign Key to Task model)
    # user_id: int (Foreign Key to User model - author of the comment)
    # text_content: str
    # created_at: datetime
    # updated_at: datetime (Optional, if comments can be edited)
    pass

class Attachment:
    """
    Represents a file or link attached to a task.
    """
    # id: int (Primary Key)
    # task_id: int (Foreign Key to Task model)
    # user_id: int (Foreign Key to User model - who uploaded/attached)
    # file_name: str (Optional, if direct upload)
    # file_url: str (Link to external storage like GDrive, S3, etc.)
    # attachment_type: str (e.g., "link", "file_upload")
    # uploaded_at: datetime
    pass
