# src/clients/models.py
# Placeholder for client data model
# Assuming a Python/Django-like ORM structure for now

class Client:
    """
    Represents a client account (sub-account) managed by the agency.
    """
    # id: int (Primary Key)
    # name: str (Client's official name or brand name) - Unique
    # contact_person_name: str (Optional)
    # contact_email: str (Optional)
    # contact_phone: str (Optional)
    #
    # # Information from Intake Form (can be stored as structured JSON or individual fields)
    # brand_information: dict # (e.g., logo_url, brand_colors, font_preferences, style_guide_url)
    # social_media_goals: str # (Text description of goals, KPIs)
    # content_preferences: dict # (e.g., types_of_content, preferred_tone_voice, example_links)
    # existing_assets_links: list[str] # (Links to Google Drive, Dropbox, etc.)
    # timeline_and_volume_expectations: str # (e.g., "2 videos per week", "major campaign in Q3")
    # customer_experience_vision: str # (Description of desired CX, e.g., "Disney-level, magical")
    #
    # # Account Status & Management
    # sub_account_status: str # (e.g., "Active", "Inactive", "Onboarding")
    # onboarded_at: datetime (Optional)
    # created_at: datetime
    # updated_at: datetime
    #
    # # Foreign Keys / Relationships
    # # tasks: list[Task] (One-to-Many relationship with Task model)
    # # users: list[User] (One-to-Many relationship for client-specific users, or Many-to-Many if agency users can be assigned to multiple clients)
    # # social_media_connections: list[SocialMediaConnection] (Details of connected social accounts)
    pass

class SocialMediaConnection:
    """
    Stores details for a client's connected social media account.
    (Could also be part of a broader 'Integrations' model)
    """
    # id: int (Primary Key)
    # client_id: int (Foreign Key to Client model)
    # platform_name: str (e.g., "Facebook", "Instagram", "YouTube", "LinkedIn")
    # account_id_on_platform: str (e.g., Page ID, Channel ID)
    # access_token: str (Encrypted)
    # refresh_token: str (Encrypted, if applicable)
    # token_expires_at: datetime (Optional)
    # permissions_granted: list[str] (e.g., ["post_content", "read_analytics"])
    # connected_at: datetime
    # last_successful_sync: datetime (Optional)
    pass
