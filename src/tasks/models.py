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
    # status: str (e.g., "To-Do", "In Progress", "In Review", "Done", "Waiting for Approval")
    # priority: str (e.g., "Low", "Medium", "High", "Urgent")
    # due_date: date (Optional)
    # created_at: datetime
    # updated_at: datetime
    #
    # # Relationships
    # client_id: int (Foreign Key to Client model, Nullable) - Associates task with a specific client project.
    #                                                        - Null for internal agency tasks.
    # assignee_id: int (Foreign Key to User model, Nullable) - User responsible for completing the task.
    # reporter_id: int (Foreign Key to User model) - User who created or reported the task.
    # project_id: int (Foreign Key to Project model, Nullable) - If tasks are grouped into larger projects.
    #
    # # Content Workflow related fields (could be in a separate model/table linked to task if complex)
    # raw_content_link: str (Optional, e.g., link to Google Drive for raw footage)
    # script_or_brief_link: str (Optional, e.g., link to Google Doc)
    # edited_content_link: str (Optional, e.g., link to edited video)
    # approval_status: str (Optional, e.g., "Pending Review", "Changes Requested", "Approved")
    # reviewer_id: int (Foreign Key to User model, Nullable) - User responsible for approving content.
    #
    # # Attachments & Comments (likely separate models with Many-to-One relationship to Task)
    # # attachments: list[Attachment]
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
