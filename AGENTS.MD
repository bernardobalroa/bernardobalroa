# AGENTS.MD - Guidelines for AI-Assisted Development

This document provides guidelines for AI agents working on the Agency Management Platform project.

## 1. Project Phasing and Focus

*   **Adhere to Phased Development:** The project will be developed in phases as outlined in the main project overview. Ensure that features align with the current development phase.
    *   Phase 1: Core task management and client accounts (basic CRM).
    *   Phase 2: Content workflow and Google Drive integration.
    *   Phase 3: Social media API integration.
    *   Phase 4: AI transcription and description generation.
    *   Phase 5: AI client agent.
    *   Phase 6: Polishing features (analytics, reminders).
*   **Current Focus:** We are currently in **Phase 2: Content workflow and Google Drive integration**.
    *   Prioritize refining Task models and services for content lifecycle (upload, review, approval).
    *   Focus on clear status transitions for content (`content_status`).
    *   Implement user notifications for key workflow steps (e.g., content ready for review, changes requested, content approved).
    *   For Google Drive integration, MVP will be simple URL linking; API integration is a future enhancement. (See `docs/google_drive_integration_strategy.md`).

## 2. Technology Stack

*   **Frontend:** A modern JavaScript framework (e.g., React, Vue) is planned. Specific choices will be made later.
*   **Backend:** Node.js/Express or Python/Django are the primary considerations. For initial model definitions, Python/Django style placeholders can be used.
*   **Database:** A relational database (e.g., PostgreSQL, MySQL) is preferred, especially due to the multi-tenant nature of the application.
*   **AI Components:**
    *   Transcription: OpenAI Whisper (self-hosted if possible) or other cost-effective/free accurate APIs.
    *   LLM: OpenAI GPT-4 API or equivalent, potentially fine-tuned or using RAG with vector databases (e.g., FAISS, Pinecone).
    *   Prioritize cost-effective or open-source solutions where quality is not compromised.

## 3. Design Principles

*   **Modular Design:** Build components and modules in a way that they are loosely coupled and can be developed, tested, and scaled independently. This is crucial for managing the complexity of the platform.
*   **Multi-Tenancy:** This is a core requirement.
    *   Ensure strict data isolation between clients at the database and application logic level.
    *   All data models should have a clear `client_id` or equivalent mechanism for segregation.
*   **Security First:**
    *   Implement RBAC thoroughly for all user roles.
    *   Securely manage API keys and client credentials (e.g., encryption at rest, secure storage).
    *   Be mindful of common web vulnerabilities (XSS, CSRF, SQL Injection).
*   **Scalability:** Design with future growth in mind. Consider stateless application services where possible and efficient database querying.

## 4. Coding Conventions (Initial)

*   **Clarity and Readability:** Write code that is easy to understand and maintain.
*   **Comments:** Add comments to explain complex logic, assumptions, or important decisions.
*   **Naming Conventions:** Use consistent and descriptive names for variables, functions, classes, and files. (Specific conventions will be defined per language/framework).
*   **Error Handling:** Implement robust error handling and logging.

## 5. AI Agent Collaboration

*   **Iterative Development:** Work in small, manageable steps.
*   **Planning:** Always create a plan before making significant code changes. Use the `set_plan` tool.
*   **Communication:** Clearly state actions taken and seek clarification when requirements are ambiguous.
*   **Tool Usage:** Utilize available tools effectively. Read files, search, and verify changes.
*   **Testing:** While full TDD might be implemented later, always consider how your changes will be tested. Create unit tests where appropriate.

## 6. Adherence to Project Overview

*   The main project overview document is the primary source of truth for requirements and features. Refer to it frequently.
*   If any conflicts arise between these guidelines and the main project overview, the main overview takes precedence.

This document will be updated as the project progresses.
