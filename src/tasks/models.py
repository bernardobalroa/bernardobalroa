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
    # assignee_id: int (Foreign Key to User model, Nullable) - User primarily responsible for the overall task. Specific content assets can have their own assignees.
    # reporter_id: int (Foreign Key to User model) - User who created or reported the task.
    # project_id: int (Foreign Key to Project model, Nullable) - If tasks are grouped into larger projects.
    # # reviewer_id: int (Foreign Key to User model, Nullable) - This is now moved to ContentAsset. A task might have an overall "approver" or "manager" if needed, but content review is per-asset.
    #
    # # Content Workflow Specific Fields have been moved to ContentAsset model.
    # # The Task model now focuses on the overall deliverable or project stage.
    # # Individual content pieces (videos, blogs, graphics) associated with this task
    # # are managed as ContentAsset records linked to this task_id.
    #
    # # Attachments & Comments (likely separate models with Many-to-One relationship to Task)
    # # attachments: list[Attachment] # General task attachments (e.g., meeting notes, overall brief not tied to one asset)
    # # comments: list[Comment] # General task comments
    # # content_assets: list[ContentAsset] (One-to-Many relationship: A task can have multiple content assets)
    pass


class ContentAsset:
    """
    Represents a single piece of content (e.g., a video, a blog post, an image) associated with a Task.
    Each asset can have its own workflow, links, and versions.
    """
    # id: int (Primary Key)
    # task_id: int (Foreign Key to Task model, identifying which task this asset belongs to)
    # name: str (Optional, user-defined name for this asset, e.g., "Intro Video - Draft 1", "Hero Image for Social")
    # asset_type: str (e.g., "video", "blog_post", "social_graphic", "script", "brief", "raw_footage")
    #   - Helps in categorizing and potentially handling different asset types differently.
    #
    # # Workflow and Versioning for this specific asset
    # content_status: str (e.g., "NotStarted", "RawUploaded", "EditingInProgress", "PendingReview", "ChangesRequested", "Approved", "Archived")
    #   - Status specific to this asset's lifecycle.
    # version_number: int (e.g., 1, 2, 3 - for iterative versions of this asset)
    #
    # # Links to actual content (typically external URLs, e.g., Google Drive)
    # raw_content_link: str (Optional, URL to raw materials if applicable for this asset type)
    # source_document_link: str (Optional, URL to a script, brief, or source text this asset is based on)
    # current_content_link: str (Optional, URL to the current version of the asset, e.g., edited video link, blog draft link)
    # published_url: str (Optional, URL where the final content is published, if applicable)
    #
    # # People involved with this asset
    # assignee_id: int (Foreign Key to User model, e.g., the editor currently working on this video asset)
    # reviewer_id: int (Foreign Key to User model, e.g., the person designated to review this specific asset)
    #
    # # Feedback & History
    # last_feedback_summary: str (Optional, summary of the latest review feedback for this asset)
    # # For more detailed version history, a separate ContentAssetVersion model might be linked here,
    # # or this ContentAsset itself could represent a specific version, with a parent_asset_id linking revisions.
    # # For now, `version_number` and `current_content_link` manage this simply.
    #
    # # Timestamps
    # created_at: datetime
    # updated_at: datetime
    # submitted_for_review_at: datetime (Optional)
    # approved_at: datetime (Optional)
    # published_at: datetime (Optional)
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
