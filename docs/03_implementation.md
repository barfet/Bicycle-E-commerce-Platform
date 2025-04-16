**Project Implementation Plan: Marcus's Custom Bicycle E-commerce Platform V1**

**Assumed Core Tech Stack:** Python (Flask/FastAPI), PostgreSQL, React, TypeScript.

**Methodology:** Agile (Scrum/Kanban), Test-Driven Development (TDD)

---

**EPIC-01: Foundational Setup & Core Data Modeling**

*   **ID:** EPIC-01
*   **Title:** Foundational Setup & Core Data Modeling
*   **Description:** Establish the project structure, core dependencies, database connection, and define the fundamental database models required to represent products, parts, and options, laying the groundwork for all subsequent features.
*   **Overview:** This epic covers initializing the backend (Python) and frontend (React) projects, setting up CI/CD basics, configuring the database ORM (e.g., SQLAlchemy with Alembic, or Django ORM), and creating the initial database schema based on the TDD's data model section for product types, part categories, and part options.
*   **Implementation Guidance:** Use standard project layout patterns for Flask/FastAPI and Create React App (or Vite). Implement database migrations using Alembic (if SQLAlchemy) or Django migrations. Define Pydantic models (FastAPI) or Marshmallow schemas (Flask) for data validation and serialization alongside ORM models. All database models must have corresponding unit tests ensuring constraints and relationships.
*   **Architecture Notes:** Involves setting up the main Backend API service structure, the Frontend SPA structure, and the initial PostgreSQL Database schema. Focuses on `product_types`, `part_categories`, `part_options` tables and their corresponding ORM models. No API endpoints are defined yet, only the underlying models and project setup.

    ---

    **STORY-101: Initialize Backend Project Structure & DB Setup**
    *   **ID:** STORY-101
    *   **Parent Epic ID:** EPIC-01
    *   **Description:** As a Developer, I want to initialize the Python backend project with necessary dependencies, configure database connection, and set up the ORM and migration tools so that we have a working foundation for backend development.
    *   **Overview:** Sets up the Flask/FastAPI project, installs core libraries (web framework, ORM, psycopg2, migration tool), configures environment variables (e.g., `DATABASE_URL`), and establishes basic DB connectivity.
    *   **Implementation Guidance:** Use `venv` or `conda` for environment management. Use `pip freeze > requirements.txt`. Configure Alembic or Django migrations. Ensure database connection pooling is configured.
    *   **Architecture Notes:** Creates the core Python service structure. Establishes the link between the application layer and the PostgreSQL database via the ORM.
    *   **Acceptance Criteria:**
        *   A new Flask/FastAPI project is created and runnable locally.
        *   Core dependencies are listed in `requirements.txt`.
        *   Database connection parameters are configurable via environment variables.
        *   The ORM is configured and can connect to the database.
        *   A migration tool (Alembic/Django) is initialized and can generate/apply initial migrations.

        *   **Tasks:**
            *   `(Setup) TASK-101.1: Initialize Python virtual environment and project structure (Flask/FastAPI).`
            *   `(Setup) TASK-101.2: Add core dependencies (Flask/FastAPI, SQLAlchemy/Django ORM, psycopg2, Alembic/Django, Pydantic/Marshmallow) to requirements.`
            *   `(Setup) TASK-101.3: Configure environment variable handling for database connection string.`
            *   `(Setup) TASK-101.4: Write failing test for basic database connectivity.`
            *   `(Backend/Python) TASK-101.5: Implement database connection logic (using ORM config) to pass connectivity test.`
            *   `(Setup) TASK-101.6: Initialize Alembic/Django migrations.`

    ---

    **STORY-102: Define Core Product Data Models & Migrations**
    *   **ID:** STORY-102
    *   **Parent Epic ID:** EPIC-01
    *   **Description:** As a Developer, I want to define and implement the ORM models and corresponding database migrations for `ProductType`, `PartCategory`, and `PartOption` so that the fundamental product structure can be stored and managed.
    *   **Overview:** Implements the database tables and Python ORM classes specified in the TDD's Data Model section for the core product entities.
    *   **Implementation Guidance:** Define models using SQLAlchemy declarative base or Django Models. Ensure relationships (FKs) are correctly defined with appropriate cascade/backref behavior. Include `created_at`, `updated_at` timestamp fields. Use Pydantic/Marshmallow for validation schemas corresponding to these models.
    *   **Architecture Notes:** Creates the `product_types`, `part_categories`, `part_options` tables in the PostgreSQL database and their corresponding Python representations.
    *   **Acceptance Criteria:**
        *   ORM models for `ProductType`, `PartCategory`, `PartOption` exist and match TDD specs.
        *   Unit tests exist for each model verifying fields, types, and relationships.
        *   Database migrations are generated to create these tables.
        *   Migrations can be successfully applied and rolled back.

        *   **Tasks:**
            *   `(Backend/Python) TASK-102.1: Write failing unit test for ProductType model structure and constraints.`
            *   `(Backend/Python) TASK-102.2: Implement ProductType ORM model (SQLAlchemy/Django).`
            *   `(Backend/Python) TASK-102.3: Write unit tests and implement Pydantic/Marshmallow schema for ProductType.`
            *   `(Backend/Python) TASK-102.4: Write failing unit test for PartCategory model structure, constraints, and relationship to ProductType.`
            *   `(Backend/Python) TASK-102.5: Implement PartCategory ORM model.`
            *   `(Backend/Python) TASK-102.6: Write unit tests and implement Pydantic/Marshmallow schema for PartCategory.`
            *   `(Backend/Python) TASK-102.7: Write failing unit test for PartOption model structure, constraints, and relationship to PartCategory.`
            *   `(Backend/Python) TASK-102.8: Implement PartOption ORM model (including `base_price`, `is_in_stock`).`
            *   `(Backend/Python) TASK-102.9: Write unit tests and implement Pydantic/Marshmallow schema for PartOption.`
            *   `(Backend/Python) TASK-102.10: Generate database migration(s) for the new models using Alembic/Django.`
            *   `(Infra) TASK-102.11: Apply migrations to a test database and verify schema.`

    ---

    **STORY-103: Initialize Frontend Project Structure**
    *   **ID:** STORY-103
    *   **Parent Epic ID:** EPIC-01
    *   **Description:** As a Developer, I want to initialize the React frontend project with necessary dependencies and basic structure so that we have a foundation for frontend development.
    *   **Overview:** Sets up the React project using Create React App or Vite, installs core libraries (React Router, state management library like Zustand/Redux Toolkit, Axios/fetch), and establishes basic project organization (components, services, contexts/store).
    *   **Implementation Guidance:** Use TypeScript. Set up basic routing structure (e.g., placeholder routes for Home, Admin). Configure Axios or a fetch wrapper for API calls. Choose and configure a state management library.
    *   **Architecture Notes:** Creates the core React SPA structure. No significant components or API calls yet.
    *   **Acceptance Criteria:**
        *   A new React/TypeScript project is created and runnable locally.
        *   Core dependencies (router, state management, HTTP client) are installed.
        *   Basic folder structure (components, services, etc.) is in place.
        *   Basic routing is set up with placeholder pages.

        *   **Tasks:**
            *   `(Setup) TASK-103.1: Initialize React/TypeScript project (CRA/Vite).`
            *   `(Setup) TASK-103.2: Add core dependencies (react-router-dom, zustand/redux-toolkit, axios).`
            *   `(Setup) TASK-103.3: Define basic project structure (src/components, src/pages, src/services, src/store).`
            *   `(Frontend/React) TASK-103.4: Implement basic App component with Router setup.`
            *   `(Frontend/React) TASK-103.5: Create placeholder components for Home and AdminLogin pages.`
            *   `(Setup) TASK-103.6: Configure Axios instance or fetch wrapper for API base URL (from env vars).`
            *   `(Setup) TASK-103.7: Set up basic state management store/context (if applicable).`

---

**EPIC-02: Admin Authentication & Panel Access**

*   **ID:** EPIC-02
*   **Title:** Admin Authentication & Panel Access
*   **Description:** Implement a secure login mechanism for the administrator (Marcus) to access the protected administration panel where product and rule management will occur.
*   **Overview:** This involves creating an `AdminUser` model, implementing password hashing, creating a login API endpoint that issues JWT tokens upon successful authentication, adding middleware to protect admin API routes, and building the frontend login form.
*   **Implementation Guidance:** Use `bcrypt` for password hashing in Python. Implement JWT generation and validation using a library like `PyJWT`. Store JWTs securely on the frontend (e.g., `localStorage` or `sessionStorage`, considering security implications) and send them in the `Authorization: Bearer <token>` header. Backend middleware must verify the token signature and expiration on protected routes.
*   **Architecture Notes:** Introduces the `admin_users` table and model. Creates `POST /api/admin/login` endpoint in the backend. Adds authentication middleware to the backend API service. Creates the Admin Login component in the React SPA and logic to store/send the token.

    ---

    **STORY-201: Implement Admin User Model & Secure Password Hashing**
    *   **ID:** STORY-201
    *   **Parent Epic ID:** EPIC-02
    *   **Description:** As a Developer, I want to create the `AdminUser` model with secure password hashing so that administrator credentials can be stored safely.
    *   **Overview:** Defines the `admin_users` table/model and integrates `bcrypt` for password hashing.
    *   **Implementation Guidance:** Model should include `username` (unique) and `password_hash`. Create helper functions `hash_password(plain_password)` and `check_password(plain_password, hashed_password)` using `bcrypt`.
    *   **Architecture Notes:** Adds the `admin_users` table to PostgreSQL and the corresponding ORM model in Python. Introduces password hashing logic within the backend service.
    *   **Acceptance Criteria:**
        *   `AdminUser` ORM model exists with `username` and `password_hash` fields.
        *   Database migration exists for the `admin_users` table.
        *   Unit tests exist verifying password hashing and checking functions.
        *   Passwords are never stored in plain text.

        *   **Tasks:**
            *   `(Backend/Python) TASK-201.1: Write failing unit test for AdminUser model structure.`
            *   `(Backend/Python) TASK-201.2: Implement AdminUser ORM model.`
            *   `(Backend/Python) TASK-201.3: Generate database migration for AdminUser.`
            *   `(Backend/Python) TASK-201.4: Write failing unit test for `hash_password` function.`
            *   `(Backend/Python) TASK-201.5: Implement `hash_password` using `bcrypt`.`
            *   `(Backend/Python) TASK-201.6: Write failing unit test for `check_password` function.`
            *   `(Backend/Python) TASK-201.7: Implement `check_password` using `bcrypt`.`
            *   `(Backend/Python) TASK-201.8: Refactor password utility functions.`
            *   `(Infra) TASK-201.9: Apply migration to test database.`
            *   `(Data) TASK-201.10: Create a seed script/command to create an initial admin user with a hashed password.`

    ---

    **STORY-202: Implement Admin Login API Endpoint (JWT)**
    *   **ID:** STORY-202
    *   **Parent Epic ID:** EPIC-02
    *   **Description:** As a Developer, I want to implement the `POST /api/admin/login` endpoint which validates credentials and returns a JWT token upon success so that the admin can authenticate.
    *   **Overview:** Creates the backend API endpoint for login. It takes username/password, finds the user, verifies the password using `check_password`, and generates/returns a JWT if valid.
    *   **Implementation Guidance:** Use `PyJWT` library. Configure JWT secret key via environment variables. Set a reasonable expiration time for the token. Define clear request (username, password) and response (token) schemas (Pydantic/Marshmallow).
    *   **Architecture Notes:** Defines the `POST /api/admin/login` route in the Python backend. Integrates user lookup and password checking logic. Introduces JWT generation.
    *   **Acceptance Criteria:**
        *   `POST /api/admin/login` endpoint exists.
        *   Endpoint accepts `username` and `password`.
        *   Valid credentials return a `200 OK` with a JWT token in the response body.
        *   Invalid credentials return a `401 Unauthorized` status.
        *   Integration tests cover successful login and failed login attempts.

        *   **Tasks:**
            *   `(Backend/Python) TASK-202.1: Write failing integration test for `POST /api/admin/login` with valid credentials.`
            *   `(Backend/Python) TASK-202.2: Write failing integration test for `POST /api/admin/login` with invalid credentials.`
            *   `(Backend/Python) TASK-202.3: Implement basic route structure for `POST /api/admin/login`.`
            *   `(Backend/Python) TASK-202.4: Implement request body parsing/validation (Pydantic/Marshmallow).`
            *   `(Backend/Python) TASK-202.5: Implement database lookup logic for AdminUser by username.`
            *   `(Backend/Python) TASK-202.6: Implement password verification logic using `check_password`.`
            *   `(Backend/Python) TASK-202.7: Write failing unit test for JWT generation logic.`
            *   `(Backend/Python) TASK-202.8: Implement JWT generation logic using `PyJWT` and configured secret/expiration.`
            *   `(Backend/Python) TASK-202.9: Implement response serialization (token).`
            *   `(Backend/Python) TASK-202.10: Complete API endpoint logic to pass integration tests.`
            *   `(Backend/Python) TASK-202.11: Refactor login endpoint code.`

    ---

    **STORY-203: Implement Backend Authentication Middleware**
    *   **ID:** STORY-203
    *   **Parent Epic ID:** EPIC-02
    *   **Description:** As a Developer, I want to implement authentication middleware for the backend API so that specific admin routes can be protected and require a valid JWT token.
    *   **Overview:** Creates middleware (e.g., a Flask decorator or FastAPI dependency) that extracts the JWT from the `Authorization` header, validates it (signature, expiration), and denies access if invalid.
    *   **Implementation Guidance:** Use `PyJWT` to decode and verify the token. Handle missing token, invalid token format, expired signature, and invalid signature errors gracefully, returning `401 Unauthorized`. Optionally, attach the authenticated user's ID or object to the request context for later use.
    *   **Architecture Notes:** Adds a security layer to the backend API. This middleware will wrap all subsequent admin API endpoints.
    *   **Acceptance Criteria:**
        *   Middleware/decorator exists to protect routes.
        *   Protected routes return `401 Unauthorized` if no token or an invalid/expired token is provided.
        *   Protected routes allow access if a valid token is provided.
        *   Integration tests verify protected route access with and without valid tokens.

        *   **Tasks:**
            *   `(Backend/Python) TASK-203.1: Write failing unit test for JWT validation logic (valid, invalid signature, expired).`
            *   `(Backend/Python) TASK-203.2: Implement JWT validation logic using `PyJWT`.`
            *   `(Backend/Python) TASK-203.3: Refactor JWT validation logic.`
            *   `(Backend/Python) TASK-203.4: Write failing integration test for a dummy protected endpoint (e.g., `GET /api/admin/me`).`
            *   `(Backend/Python) TASK-203.5: Implement authentication middleware/decorator for Flask/FastAPI.`
            *   `(Backend/Python) TASK-203.6: Apply middleware to the dummy protected endpoint.`
            *   `(Backend/Python) TASK-203.7: Implement logic within the dummy endpoint (e.g., return authenticated user info if middleware attaches it).`
            *   `(Backend/Python) TASK-203.8: Ensure integration tests pass for protected route access control.`

    ---

    **STORY-204: Implement Frontend Login Form & Token Handling**
    *   **ID:** STORY-204
    *   **Parent Epic ID:** EPIC-02
    *   **Description:** As Marcus (Admin), I want a login form where I can enter my credentials and submit them, so that I can gain access to the admin panel.
    *   **Overview:** Creates the React component for the login form, handles form state, makes the API call to `POST /api/admin/login`, stores the received JWT upon success, and redirects to a placeholder admin dashboard page.
    *   **Implementation Guidance:** Use React `useState` for form fields. Use an async function with `axios` or `fetch` to call the login API. Store the token in `localStorage` or `sessionStorage`. Use React Router's `useNavigate` for redirection. Provide user feedback for loading states and login errors.
    *   **Architecture Notes:** Creates the `AdminLogin` component in the React SPA. Implements the client-side logic for calling the backend login endpoint and managing the authentication token. Sets up Axios interceptors to automatically add the `Authorization` header to subsequent requests.
    *   **Acceptance Criteria:**
        *   An admin login page exists with username and password fields and a submit button.
        *   Submitting valid credentials calls the backend API, stores the token, and redirects to the admin area.
        *   Submitting invalid credentials displays an appropriate error message.
        *   Subsequent API calls made after successful login include the `Authorization: Bearer <token>` header.

        *   **Tasks:**
            *   `(Frontend/React) TASK-204.1: Write failing unit test for basic Login Form component rendering.`
            *   `(Frontend/React) TASK-204.2: Create basic structure for `AdminLoginForm` component.`
            *   `(Frontend/React) TASK-204.3: Implement state management (`useState`) for username and password fields.`
            *   `(Frontend/React) TASK-204.4: Write failing unit test for form submission logic (mocking API call).`
            *   `(Frontend/React) TASK-204.5: Implement form submission handler.`
            *   `(Frontend/React) TASK-204.6: Implement API call logic to `POST /api/admin/login` using Axios/fetch.`
            *   `(Frontend/React) TASK-204.7: Implement logic to store JWT in localStorage/sessionStorage upon successful login.`
            *   `(Frontend/React) TASK-204.8: Implement redirection using `useNavigate` upon successful login.`
            *   `(Frontend/React) TASK-204.9: Implement error handling and display for failed login attempts.`
            *   `(Frontend/React) TASK-204.10: Refactor `AdminLoginForm` component.`
            *   `(Frontend/React) TASK-204.11: Implement Axios request interceptor to add `Authorization` header if token exists.`
            *   `(Frontend/React) TASK-204.12: Style the login form.`
            *   `(E2E Test) TASK-204.13: Write E2E test for successful admin login flow.`
            *   `(E2E Test) TASK-204.14: Write E2E test for failed admin login flow.`

---

**EPIC-03: Admin Product & Part Management (CRUD)**

*   **ID:** EPIC-03
*   **Title:** Admin Product & Part Management (CRUD)
*   **Description:** Enable the administrator (Marcus) to manage the core product catalog, including defining product types, part categories, and specific part options with their base prices and stock status.
*   **Overview:** This epic involves creating protected backend API endpoints for CRUD operations (Create, Read, Update, Delete) on `ProductType`, `PartCategory`, and `PartOption` models. It also involves building the corresponding frontend interfaces within the admin panel for Marcus to interact with this data.
*   **Implementation Guidance:** Follow RESTful principles for API design. Use the authentication middleware created in EPIC-02 to protect all endpoints. Implement proper data validation (using Pydantic/Marshmallow) for all incoming create/update requests. On the frontend, create reusable components for displaying data tables and forms. Manage frontend state effectively (Zustand/Redux Toolkit) for fetched data and form inputs.
*   **Architecture Notes:** Defines CRUD API endpoints (e.g., `GET, POST /api/admin/product-types`, `GET, PUT, DELETE /api/admin/product-types/{id}`, and similarly for categories/options). Implements backend service logic interacting with the ORM for these operations. Creates corresponding React components and views within the authenticated admin section of the SPA.

    ---
    *(Note: Stories below follow a similar Task pattern as STORY-20x, including tests first, backend implementation, frontend implementation, E2E tests. For brevity, only key tasks specific to the functionality are highlighted.)*

    **STORY-301: Implement Backend CRUD API for Product Types**
    *   **ID:** STORY-301
    *   **Parent Epic ID:** EPIC-03
    *   **Description:** As a Developer, I want to implement protected backend API endpoints for CRUD operations on `ProductType` so that admin users can manage product types.
    *   **Overview:** Creates GET (list, detail), POST, PUT, DELETE endpoints for `ProductType`.
    *   **Acceptance Criteria:** API endpoints exist, are protected, perform correct DB operations, return correct data/status codes, and are covered by integration tests.
        *   **Key Tasks:** Write integration tests for each endpoint (GET list, GET detail, POST, PUT, DELETE) ensuring auth protection. Implement Flask/FastAPI views/controllers, validation schemas, ORM logic for each operation.

    ---

    **STORY-302: Implement Frontend CRUD Interface for Product Types**
    *   **ID:** STORY-302
    *   **Parent Epic ID:** EPIC-03
    *   **Description:** As Marcus (Admin), I want an interface to view, create, edit, and delete Product Types so that I can manage the high-level categories of products I sell (e.g., Bicycles).
    *   **Overview:** Creates React components for listing product types (table) and a form for creating/editing them. Integrates API calls to the backend endpoints from STORY-301.
    *   **Acceptance Criteria:** Admin users can view a list of product types, click to edit one, save changes, create a new one, and delete one via the UI. UI updates correctly after operations.
        *   **Key Tasks:** Write component unit tests. Create React components (`ProductTypeList`, `ProductTypeForm`). Implement state management for product type data. Implement API call logic (using Axios/fetch wrapper). Write E2E tests for the full CRUD flow via the UI.

    ---

    **STORY-303: Implement Backend CRUD API for Part Categories**
    *   **ID:** STORY-303
    *   **Parent Epic ID:** EPIC-03
    *   **Description:** As a Developer, I want to implement protected backend API endpoints for CRUD operations on `PartCategory`, ensuring they are linked to a `ProductType`, so that admin users can manage part categories.
    *   **Overview:** Creates GET (list, detail), POST, PUT, DELETE endpoints for `PartCategory`. POST/PUT must include `product_type_id`.
    *   **Acceptance Criteria:** API endpoints exist, are protected, enforce `product_type_id` linkage, perform correct DB operations, return correct data/status codes, and are covered by integration tests.
        *   **Key Tasks:** Similar to STORY-301, but ensure validation and ORM logic correctly handles the foreign key relationship to `ProductType`.

    ---

    **STORY-304: Implement Frontend CRUD Interface for Part Categories**
    *   **ID:** STORY-304
    *   **Parent Epic ID:** EPIC-03
    *   **Description:** As Marcus (Admin), I want an interface to view, create, edit, and delete Part Categories (e.g., "Frame", "Wheels") associated with a specific Product Type, so that I can structure the customizable parts.
    *   **Overview:** Creates React components for listing/managing part categories, often viewed within the context of a selected Product Type.
    *   **Acceptance Criteria:** Admin users can select a Product Type and then view/manage its associated Part Categories via the UI.
        *   **Key Tasks:** Similar to STORY-302, but components need to handle filtering/displaying based on the selected `product_type_id`. E2E tests should cover CRUD within the context of a product type.

    ---

    **STORY-305: Implement Backend CRUD API for Part Options**
    *   **ID:** STORY-305
    *   **Parent Epic ID:** EPIC-03
    *   **Description:** As a Developer, I want to implement protected backend API endpoints for CRUD operations on `PartOption`, including setting `base_price` and `is_in_stock`, ensuring they are linked to a `PartCategory`, so that admin users can manage specific part choices.
    *   **Overview:** Creates GET (list, detail), POST, PUT, DELETE endpoints for `PartOption`. POST/PUT must include `part_category_id`, `base_price`, and optionally `is_in_stock` (defaults to true). PUT should allow updating price and stock status independently.
    *   **Acceptance Criteria:** API endpoints exist, are protected, enforce linkage and required fields, perform correct DB operations (including price/stock updates), return correct data/status codes, and are covered by integration tests.
        *   **Key Tasks:** Similar to STORY-303, handling `base_price` and `is_in_stock` fields in validation, ORM logic, and tests. Need specific tests for updating only stock or only price.

    ---

    **STORY-306: Implement Frontend CRUD Interface for Part Options (including Stock Toggle)**
    *   **ID:** STORY-306
    *   **Parent Epic ID:** EPIC-03
    *   **Description:** As Marcus (Admin), I want an interface to view, create, edit (price), and delete Part Options (e.g., "Full-suspension", "Red Rim") associated with a Part Category, and quickly toggle their stock status, so that I can manage my inventory and pricing.
    *   **Overview:** Creates React components for managing part options within the context of a selected Part Category. Includes specific UI elements for setting price and a toggle/button for `is_in_stock`.
    *   **Acceptance Criteria:** Admin users can select a Part Category and manage its options. Price can be edited. Stock status can be toggled with immediate feedback (via API call).
        *   **Key Tasks:** Similar to STORY-304. Add input for `base_price`. Implement a toggle/button component that triggers a specific API call (e.g., a dedicated PATCH endpoint or PUT with only the stock field) to update `is_in_stock` efficiently. Update E2E tests.

---

**EPIC-04: Admin Rule Management (Compatibility & Pricing)**

*   **ID:** EPIC-04
*   **Title:** Admin Rule Management (Compatibility & Pricing)
*   **Description:** Enable the administrator (Marcus) to define and manage the complex compatibility and pricing rules that govern how bicycles can be configured and how their final price is calculated.
*   **Overview:** This is a complex epic. It involves creating the database models for rules (`compatibility_rules`, `pricing_rules`), implementing backend APIs for CRUD operations on these rules, and designing intuitive frontend interfaces for Marcus to define potentially complex conditional logic without writing code.
*   **Implementation Guidance:** The structure for storing rules (simple FKs vs. JSONB) needs careful implementation based on TDD refinement. The backend API needs robust validation to prevent impossible or contradictory rules where feasible. The frontend UI is critical – consider a rule builder interface (e.g., dropdowns for selecting parts/options, conditions like "IF", "AND", "THEN", "EXCLUDES", "SET PRICE"). Test rule logic extensively.
*   **Architecture Notes:** Introduces `compatibility_rules` and `pricing_rules` tables/models. Defines CRUD API endpoints (e.g., `/api/admin/rules/compatibility`, `/api/admin/rules/pricing`). Implements backend logic for rule validation and persistence. Creates specialized React components for rule definition in the admin panel.

    ---
    *(Stories follow similar TDD Task patterns. Focus on the specific challenges of rule management.)*

    **STORY-401: Define Rule Data Models & Migrations**
    *   **ID:** STORY-401
    *   **Parent Epic ID:** EPIC-04
    *   **Description:** As a Developer, I want to define and implement the ORM models and migrations for `CompatibilityRule` and `PricingRule` according to the TDD, so that rules can be stored.
    *   **Overview:** Implements the database tables and Python ORM classes for rules, deciding on simple FKs or JSONB for conditions based on TDD.
    *   **Acceptance Criteria:** Models and migrations exist, match TDD, pass unit tests.
        *   **Key Tasks:** Implement models (SQLAlchemy/Django), Pydantic/Marshmallow schemas, unit tests, generate/apply migrations. Pay close attention to the structure chosen for conditions (`condition_options` in `pricing_rules`).

    ---

    **STORY-402: Implement Backend CRUD API for Compatibility Rules**
    *   **ID:** STORY-402
    *   **Parent Epic ID:** EPIC-04
    *   **Description:** As a Developer, I want to implement protected backend API endpoints for CRUD operations on `CompatibilityRule` so that admins can manage exclusion rules.
    *   **Overview:** Creates GET, POST, PUT, DELETE endpoints for compatibility rules, likely scoped by `product_type_id`. Validation is key.
    *   **Acceptance Criteria:** Endpoints exist, are protected, perform validation (e.g., ensure trigger/target options exist and belong to the correct product type), perform DB ops, tested.
        *   **Key Tasks:** Write integration tests. Implement views/controllers, validation, ORM logic. Focus on validation logic for rule integrity.

    ---

    **STORY-403: Implement Frontend UI for Compatibility Rule Management**
    *   **ID:** STORY-403
    *   **Parent Epic ID:** EPIC-04
    *   **Description:** As Marcus (Admin), I want an intuitive interface to define compatibility rules (e.g., "IF [Part A Option X] selected, THEN [Part B Option Y] is unavailable") so that I can prevent impossible configurations.
    *   **Overview:** Creates the React UI for defining these rules. This likely involves dropdowns populated with available part options based on the selected product type.
    *   **Acceptance Criteria:** Admin can view existing rules, create new rules by selecting trigger/target options, edit, and delete rules via the UI. UI prevents illogical selections where possible.
        *   **Key Tasks:** Design and implement the rule builder UI component(s). Fetch necessary part options data to populate dropdowns dynamically. Implement API calls. Write E2E tests.

    ---

    **STORY-404: Implement Backend CRUD API for Pricing Rules**
    *   **ID:** STORY-404
    *   **Parent Epic ID:** EPIC-04
    *   **Description:** As a Developer, I want to implement protected backend API endpoints for CRUD operations on `PricingRule` so that admins can manage conditional pricing.
    *   **Overview:** Creates GET, POST, PUT, DELETE endpoints for pricing rules. Handling the `condition_options` (potentially JSONB array of option IDs) and `new_price` is key.
    *   **Acceptance Criteria:** Endpoints exist, are protected, handle potentially complex condition structures, validate input, perform DB ops, tested.
        *   **Key Tasks:** Write integration tests. Implement views/controllers, validation (especially for `condition_options` structure), ORM logic. Handle `priority` field if implemented.

    ---

    **STORY-405: Implement Frontend UI for Pricing Rule Management**
    *   **ID:** STORY-405
    *   **Parent Epic ID:** EPIC-04
    *   **Description:** As Marcus (Admin), I want an intuitive interface to define pricing rules (e.g., "IF [Option A] AND [Option B] are selected, THEN price of [Option C] becomes [Z EUR]") so that I can handle complex pricing dependencies.
    *   **Overview:** Creates the React UI for pricing rules. This is likely more complex than compatibility, potentially allowing selection of multiple condition options.
    *   **Acceptance Criteria:** Admin can view, create (selecting multiple condition options, target option, new price), edit, and delete pricing rules via the UI.
        *   **Key Tasks:** Design and implement the pricing rule builder UI. Handle selection of multiple condition options. Implement API calls. Write E2E tests. Requires careful state management.

---

**EPIC-05: Core Configuration Logic (Rule Engine Backend)**

*   **ID:** EPIC-05
*   **Title:** Core Configuration Logic (Rule Engine Backend)
*   **Description:** Implement the backend logic that takes a set of selected part options, applies all relevant compatibility and pricing rules, and determines the final valid configuration state and accurate price.
*   **Overview:** This epic focuses entirely on the backend. It involves creating the "Rule Engine" module described in the TDD. This module will contain the core algorithms for evaluating compatibility (which options are available/unavailable) and calculating the final price based on selected options and defined rules. It culminates in the `POST /api/products/{productTypeId}/evaluate` endpoint.
*   **Implementation Guidance:** This is performance-sensitive. Optimize database queries to fetch relevant rules efficiently (caching is highly recommended here - Redis). The evaluation logic needs to be robust and handle rule priorities correctly (especially for pricing). Write extensive unit tests covering various rule interaction scenarios.
*   **Architecture Notes:** Implements the `Rule Engine Module` within the Python backend service. Defines the critical `POST /api/products/{productTypeId}/evaluate` endpoint. Heavily interacts with the rule tables (`compatibility_rules`, `pricing_rules`) and part option data. May introduce caching (Redis).

    ---

    **STORY-501: Implement Compatibility Rule Evaluation Logic**
    *   **ID:** STORY-501
    *   **Parent Epic ID:** EPIC-05
    *   **Description:** As a Developer, I want to implement the backend logic that takes a list of selected `PartOption` IDs and returns a list of all other `PartOption` IDs that are incompatible based on defined `CompatibilityRule`s, so that the frontend knows which options to disable.
    *   **Overview:** Creates a Python function/class method within the Rule Engine module. Fetches relevant rules and determines excluded options.
    *   **Implementation Guidance:** Optimize DB query to get rules based on selected options. Logic should handle "EXCLUDES" rules. Consider caching rule data.
    *   **Architecture Notes:** Core part of the Rule Engine module. Reads from `compatibility_rules` and `part_options`.
    *   **Acceptance Criteria:**
        *   Function exists and takes a list of selected option IDs.
        *   Correctly identifies and returns incompatible option IDs based on various rule scenarios.
        *   Unit tests cover simple exclusions, multiple exclusions triggered, no exclusions.
        *   Performance is acceptable under simulated load (define target).

        *   **Key Tasks:** Write failing unit tests for various compatibility scenarios. Implement DB query logic (potentially cached). Implement the evaluation algorithm. Refactor.

    ---

    **STORY-502: Implement Pricing Rule Evaluation Logic**
    *   **ID:** STORY-502
    *   **Parent Epic ID:** EPIC-05
    *   **Description:** As a Developer, I want to implement the backend logic that takes a list of selected `PartOption` IDs, calculates the base price, and applies relevant `PricingRule`s to determine the final adjusted price, so that accurate pricing can be displayed.
    *   **Overview:** Creates a Python function/class method. Calculates sum of `base_price` for selected options. Fetches relevant pricing rules based on selections. Applies matching rules (considering priority) to adjust the total price.
    *   **Implementation Guidance:** Handle rule conditions (potentially checking subsets in the `condition_options` JSONB array). Implement priority logic if multiple rules match. Optimize rule fetching (caching).
    *   **Architecture Notes:** Core part of the Rule Engine module. Reads from `pricing_rules` and `part_options`.
    *   **Acceptance Criteria:**
        *   Function exists and takes a list of selected option IDs.
        *   Correctly calculates the base price.
        *   Correctly identifies and applies matching pricing rules.
        *   Handles rule priorities correctly if applicable.
        *   Returns the accurate final price.
        *   Unit tests cover no rules, single rule match, multiple rule matches (with/without priority).
        *   Performance is acceptable.

        *   **Key Tasks:** Write failing unit tests for various pricing scenarios. Implement base price calculation. Implement DB query/cache logic for pricing rules. Implement the rule matching and price adjustment algorithm (incl. priority). Refactor.

    ---

    **STORY-503: Implement Configuration Evaluation API Endpoint**
    *   **ID:** STORY-503
    *   **Parent Epic ID:** EPIC-05
    *   **Description:** As a Developer, I want to implement the `POST /api/products/{productTypeId}/evaluate` endpoint which uses the rule engine logic to return the current valid configuration state (available/unavailable options) and the calculated price based on the user's selections, so that the frontend can update dynamically.
    *   **Overview:** Creates the main API endpoint that orchestrates calls to the compatibility and pricing evaluation logic developed in previous stories.
    *   **Implementation Guidance:** Validate input (list of selected option IDs). Call the compatibility evaluator. Call the pricing evaluator. Structure the response payload as defined in the TDD (total price, breakdown of available/unavailable options per category, potentially with reasons).
    *   **Architecture Notes:** Defines the `POST /api/products/{productTypeId}/evaluate` route. Integrates the Rule Engine module components. Defines the key data contract between backend and frontend for configuration updates.
    *   **Acceptance Criteria:**
        *   Endpoint exists and accepts a list of selected option IDs.
        *   Returns `200 OK` with the correct response structure (price, available/unavailable options per category).
        *   Correctly reflects compatibility rules in the availability status.
        *   Correctly reflects pricing rules in the total price.
        *   Handles invalid input gracefully (`400 Bad Request`).
        *   Integration tests cover various valid and invalid input scenarios and rule combinations.

        *   **Key Tasks:** Write failing integration tests. Implement endpoint route/controller. Implement request validation. Integrate calls to compatibility and pricing logic. Implement response serialization. Ensure tests pass.

---

**EPIC-06: Customer Product Configuration UI**

*   **ID:** EPIC-06
*   **Title:** Customer Product Configuration UI
*   **Description:** Develop the customer-facing user interface that allows users to select a product (bicycle), customize it by choosing part options, see real-time updates on price and compatibility, and be aware of stock status.
*   **Overview:** This epic focuses on the frontend React application. It involves fetching the initial product configuration structure, displaying part categories and options, handling user selections, calling the backend `evaluate` endpoint, and dynamically updating the UI based on the response (disabling options, showing stock status, updating price).
*   **Implementation Guidance:** Fetch initial config data using `useEffect`. Manage the state of selected options (`useState` or state management library). On option change, debounce the call to the backend `evaluate` endpoint to avoid excessive requests. Clearly visualize available, selected, incompatible, and out-of-stock options. Display the total price prominently.
*   **Architecture Notes:** Implements the main customer-facing view/page in the React SPA. Interacts heavily with `GET /api/products/{productTypeId}/configuration` (initial load) and `POST /api/products/{productTypeId}/evaluate` (on changes). Requires robust state management on the frontend.

    ---

    **STORY-601: Fetch and Display Initial Product Configuration**
    *   **ID:** STORY-601
    *   **Parent Epic ID:** EPIC-06
    *   **Description:** As a Customer, I want to see the available part categories and their options when I view a customizable product page, so that I know what I can configure.
    *   **Overview:** Creates the main React component for the product configuration page. Fetches the initial configuration structure (categories, options, base prices, stock) from the backend upon loading.
    *   **Implementation Guidance:** Use `useEffect` hook for the initial data fetch from `GET /api/products/{productTypeId}/configuration`. Store the configuration structure in component state or global store. Render categories and options based on fetched data. Handle loading and error states.
    *   **Architecture Notes:** Creates the `ProductConfigurator` component. Implements the initial API call (`GET /configuration`). Populates the UI structure.
    *   **Acceptance Criteria:**
        *   Product page loads and displays categories and options fetched from the backend.
        *   Initial stock status is displayed correctly.
        *   Loading state is shown during fetch.
        *   Error message is shown if fetching fails.

        *   **Key Tasks:** Write component tests (mocking API). Create component structure. Implement `useEffect` data fetch. Implement rendering logic for categories/options. Implement loading/error states. Style basic layout.

    ---

    **STORY-602: Handle User Selections and Update Configuration State**
    *   **ID:** STORY-602
    *   **Parent Epic ID:** EPIC-06
    *   **Description:** As a Customer, I want to be able to select an option for each part category, and have the system remember my choices, so that I can build my desired configuration.
    *   **Overview:** Implements the state management for tracking the user's selected option for each category. Updates the UI to visually indicate the selected option.
    *   **Implementation Guidance:** Use `useState` or a reducer/store to hold the map of `categoryId -> selectedOptionId`. Implement click handlers on options to update this state. Visually highlight selected options.
    *   **Architecture Notes:** Focuses on frontend state management within the `ProductConfigurator` component.
    *   **Acceptance Criteria:**
        *   Clicking an option selects it visually.
        *   Only one option per mandatory category can be selected at a time.
        *   The component's internal state accurately reflects the user's selections.

        *   **Key Tasks:** Write unit tests for selection logic. Implement state hook/reducer. Implement click handlers. Implement visual styling for selected state.

    ---

    **STORY-603: Integrate Dynamic Evaluation and UI Updates**
    *   **ID:** STORY-603
    *   **Parent Epic ID:** EPIC-06
    *   **Description:** As a Customer, when I make a selection, I want the interface to immediately update to show me which other options become unavailable (due to compatibility or stock) and what the new total price is, so that I have real-time feedback.
    *   **Overview:** Triggers a call to the backend `POST /evaluate` endpoint whenever the user changes a selection. Updates the UI based on the response: disable/grey-out incompatible/OOS options, update the displayed total price.
    *   **Implementation Guidance:** Use `useEffect` hook that triggers when the selection state changes. Debounce the API call within the effect. Update component state with the price and availability info from the API response. Conditionally render options (enabled/disabled/styled) based on this state.
    *   **Architecture Notes:** Connects the frontend selection state to the backend Rule Engine via the `/evaluate` API call. Implements the dynamic update loop.
    *   **Acceptance Criteria:**
        *   Changing an option triggers a call to the `/evaluate` API.
        *   The displayed total price updates correctly based on the API response.
        *   Options identified as incompatible or out-of-stock in the API response are visually disabled/indicated in the UI.
        *   Available options remain selectable.

        *   **Key Tasks:** Write component tests (mocking API response). Implement `useEffect` to watch selections and call `/evaluate` (with debounce). Implement logic to update price display and option availability state based on API response. Implement conditional styling/disabling of options. Write E2E tests covering dynamic updates based on selections and rules.

---

**EPIC-07: Shopping Cart (V1 - Add to Cart)**

*   **ID:** EPIC-07
*   **Title:** Shopping Cart (V1 - Add to Cart)
*   **Description:** Allow customers to add their fully configured bicycle (including all selected options and the final price) to a simple shopping cart.
*   **Overview:** For V1, this involves adding an "Add to Cart" button to the configuration page. Clicking this button sends the configuration details to a backend endpoint which stores it (likely in the user's session). A basic cart view might display the added items.
*   **Implementation Guidance:** Backend: Use server-side sessions (e.g., Flask-Session, Django sessions) stored in memory, Redis, or the database. Frontend: Implement the button click handler to POST the configuration details (`productTypeId`, selected `optionId` list, final `price`) to the backend. Optionally create a simple cart display component.
*   **Architecture Notes:** Defines `POST /api/cart` and potentially `GET /api/cart` endpoints. Implements session handling in the backend. Adds the "Add to Cart" button and cart interaction logic to the React SPA.

    ---

    **STORY-701: Implement Backend "Add to Cart" Logic (Session)**
    *   **ID:** STORY-701
    *   **Parent Epic ID:** EPIC-07
    *   **Description:** As a Developer, I want to implement the `POST /api/cart` endpoint which takes a product configuration and stores it in the user's server-side session, so that configurations can be added to the cart.
    *   **Overview:** Creates the backend endpoint and logic to add items to the session cart.
    *   **Implementation Guidance:** Configure server-side session middleware (e.g., Flask-Session with filesystem/Redis backend). The endpoint receives the configuration and appends it to a list stored in `session['cart']`.
    *   **Architecture Notes:** Introduces session management to the backend. Defines the `POST /api/cart` endpoint.
    *   **Acceptance Criteria:**
        *   Endpoint exists.
        *   Successfully adds the received configuration details to the session cart.
        *   Returns `200 OK` or `201 Created`.
        *   Handles multiple additions correctly.
        *   Integration tests verify item addition to the session.

        *   **Key Tasks:** Configure session middleware. Write integration tests. Implement endpoint view/controller. Implement logic to add item to `session['cart']`.

    ---

    **STORY-702: Implement Frontend "Add to Cart" Button**
    *   **ID:** STORY-702
    *   **Parent Epic ID:** EPIC-07
    *   **Description:** As a Customer, after configuring my bike, I want to click an "Add to Cart" button so that my configuration is saved for potential purchase.
    *   **Overview:** Adds the button to the `ProductConfigurator` component and implements the click handler to POST the current configuration to the backend.
    *   **Implementation Guidance:** Button should likely be enabled only when a valid configuration is complete (TBD based on UX). Click handler gathers `productTypeId`, selected option IDs, and final price from state and sends to `POST /api/cart`. Provide user feedback (e.g., button text changes, success message).
    *   **Architecture Notes:** Modifies the `ProductConfigurator` component. Implements the client-side logic for the "Add to Cart" action.
    *   **Acceptance Criteria:**
        *   "Add to Cart" button is present on the configuration page.
        *   Clicking the button sends the correct configuration data to the backend `POST /api/cart` endpoint.
        *   User receives feedback upon successful addition.

        *   **Key Tasks:** Write component tests. Add button element. Implement click handler. Implement API call logic. Implement user feedback. Write E2E test for adding an item to the cart.

    ---
    *(Optional V1 Story: Implement Basic Cart Display - GET /api/cart endpoint and a simple React component to display session['cart'] contents)*

---

**EPIC-08: Deployment & Initial Setup**

*   **ID:** EPIC-08
*   **Title:** Deployment & Initial Setup
*   **Description:** Prepare the application for deployment, set up the necessary cloud infrastructure, and configure CI/CD pipelines.
*   **Overview:** This covers containerizing the application (backend/frontend), setting up hosting environments (Dev/Staging/Prod) on a cloud provider (AWS/GCP/Azure), configuring managed database/cache services, and building automated deployment pipelines.
*   **Implementation Guidance:** Use Docker (`Dockerfile` for Python backend, multi-stage build for React SPA served via Nginx/Caddy). Use Terraform or CloudFormation for Infrastructure as Code (IaC). Set up GitHub Actions/GitLab CI/Jenkins for build, test, and deploy steps. Configure monitoring and logging.
*   **Architecture Notes:** Focuses on infrastructure, build, and deployment processes. Ties together the backend service, frontend build artifacts, database, and potentially cache.

    ---
    *(Stories/Tasks would cover Dockerization, CI/CD Pipeline Setup, Cloud Resource Provisioning (VPC, DB, Cache, Compute/Container Service), Environment Configuration, Monitoring Setup etc. These are often more infrastructure/DevOps focused tasks.)*

---