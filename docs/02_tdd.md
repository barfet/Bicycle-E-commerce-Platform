**Technical Design Document: Marcus's Custom Bicycle E-commerce Platform V1**

**Version:** 1.0
**Date:** April 16, 2025
**Author:** Roman Borysenok
**Related PRD:** Marcus's Custom Bicycle E-commerce Platform PRD V1.0

**1. Introduction / Overview**

This document outlines the technical design for the first version (V1) of Marcus's Custom Bicycle E-commerce Platform. The goal is to create a web application enabling customers to visually configure custom bicycles based on available parts, options, compatibility rules, and real-time pricing, and add them to a cart. It also includes an administration interface for Marcus to manage products, parts, options, stock, and the governing rules (compatibility and pricing). This design directly addresses the requirements specified in the associated PRD V1.0.

**2. Goals & Non-Goals (Technical)**

**Goals:**

*   Implement a flexible data model capable of representing customizable products, parts, options, stock status, and complex interdependencies (compatibility and pricing rules).
*   Develop a robust backend API serving both the customer-facing configuration UI and the administration panel.
*   Create an efficient "Configuration Service" or "Rule Engine" capable of evaluating compatibility and calculating prices dynamically based on user selections and defined rules.
*   Build intuitive frontend interfaces for both customer configuration and administration tasks (especially rule management).
*   Ensure the system is reliable, provides accurate configurations/pricing, and performs well under expected load.
*   Design the architecture with future scalability in mind (adding new product types beyond bicycles).

**Non-Goals (for V1):**

*   Implementation of a full checkout and payment processing workflow.
*   Customer user account creation, login, or persistent saved configurations/order history.
*   Advanced analytics or reporting features beyond basic monitoring.
*   Integration with external inventory or ERP systems.
*   Support for multiple languages or currencies (Assume single language/currency - EUR).
*   Dynamically changing product imagery based on selections.

**3. Proposed Solution / Architecture**

We propose a standard N-Tier Web Application Architecture:

*   **Frontend:** A Single Page Application (SPA) providing two distinct user experiences:
    *   Customer Configuration UI
    *   Admin Management UI
    *   The SPA will communicate with the backend via a RESTful API.
*   **Backend:** A stateless RESTful API service responsible for:
    *   Serving product data.
    *   Handling configuration logic (rule evaluation, pricing).
    *   Managing cart state (likely session-based for V1).
    *   Handling administrative CRUD operations.
    *   Authenticating/authorizing admin users.
*   **Database:** A relational database to store structured product information, rules, and potentially session/cart data if needed beyond simple session storage.
*   **Rule Engine:** Implemented as a core module within the backend service, responsible for interpreting the stored rules and applying them during configuration evaluation.

```
+-----------------+      +-----------------+      +----------------+      +----------------+
|  Customer       | ---> | Frontend SPA    | ---> | Backend API    | ---> | Database       |
|  (Browser)      |      | (React/Vue/...) |      | (Node/Python/..) |      | (PostgreSQL)   |
+-----------------+      +-------+---------+      +-------+--------+      +----------------+
                                 |                       |
                                 |                       |
+-----------------+      +-------+---------+      +-------+--------+
|  Admin (Marcus) | ---> | Admin UI (SPA)  | ---> | (Same Backend  |
|  (Browser)      |      |                 |      |  API w/ Auth)  |
+-----------------+      +-----------------+      +----------------+
                                                         |
                                                         +--> Rule Engine Module
```

**4. Detailed Design / Component Breakdown**

*   **Frontend (SPA):**
    *   `Customer Configuration View`:
        *   Fetches product structure (`GET /products/{id}/configuration`).
        *   Displays part categories and options.
        *   On user selection, sends current selections (`POST /products/{id}/evaluate`).
        *   Receives updated available options, stock status, and price; updates UI accordingly.
        *   Handles disabling/indicating incompatible/out-of-stock options.
        *   Handles "Add to Cart" action (`POST /cart`).
    *   `Shopping Cart View`:
        *   Displays items added to the cart (`GET /cart`).
    *   `Admin Login View`:
        *   Handles admin credentials input and submission (`POST /admin/login`).
    *   `Admin Dashboard`:
        *   Provides navigation to CRUD interfaces.
    *   `Admin CRUD Views (ProductType, PartCategory, PartOption, Rules)`:
        *   Generic interfaces for listing, creating, editing, deleting entities via respective Admin API endpoints.
        *   Special attention needed for Rule definition UI to make it intuitive (e.g., condition builder).
        *   Includes interface for toggling `is_in_stock` on `PartOptions`.

*   **Backend (API Service):**
    *   `API Router`: Directs incoming HTTP requests to appropriate controllers/handlers.
    *   `Auth Middleware`: Protects admin endpoints, verifies JWT tokens.
    *   `Product Controller/Service`: Handles public requests for product data and configuration evaluation. Delegates rule evaluation to the Rule Engine.
    *   `Cart Controller/Service`: Manages adding/retrieving cart items (using server-side sessions for V1).
    *   `Admin Controller/Service(s)`: Handles authenticated requests for managing Products, Parts, Options, Rules, Stock. Performs CRUD operations against the database.
    *   `Rule Engine Module`:
        *   `Compatibility Evaluator`: Takes selected `PartOption` IDs, fetches relevant `CompatibilityRules` from DB (or cache), determines which other options are allowed/disallowed.
        *   `Pricing Evaluator`: Takes selected `PartOption` IDs, calculates base price sum, fetches relevant `PricingRules` from DB (or cache), applies matching rules to adjust the final price.
        *   Needs efficient querying and evaluation logic. Rule data might be cached for performance.
    *   `Persistence Layer/ORM`: Abstracts database interactions.

**5. Data Model / Schema Design**

Using a Relational Database (e.g., PostgreSQL). Key tables:

*   `product_types`
    *   `id` (PK, UUID/Serial)
    *   `name` (VARCHAR, e.g., "Bicycle", "Skis")
    *   `description` (TEXT, nullable)
    *   `created_at`, `updated_at`

*   `part_categories`
    *   `id` (PK, UUID/Serial)
    *   `product_type_id` (FK to `product_types`)
    *   `name` (VARCHAR, e.g., "Frame", "Wheels")
    *   `display_order` (INTEGER, for UI ordering)
    *   `created_at`, `updated_at`

*   `part_options`
    *   `id` (PK, UUID/Serial)
    *   `part_category_id` (FK to `part_categories`)
    *   `name` (VARCHAR, e.g., "Full-suspension", "Red")
    *   `base_price` (DECIMAL/NUMERIC)
    *   `is_in_stock` (BOOLEAN, default: true)
    *   `created_at`, `updated_at`

*   `compatibility_rules` (Representing "If X is selected, then Y is unavailable/required")
    *   `id` (PK, UUID/Serial)
    *   `product_type_id` (FK to `product_types`, scope the rule)
    *   `trigger_option_id` (FK to `part_options`, the "If X" part)
    *   `target_option_id` (FK to `part_options`, the "Y" part)
    *   `rule_type` (ENUM/VARCHAR, e.g., 'EXCLUDES', 'REQUIRES') - *Note: 'REQUIRES' adds complexity, focus on 'EXCLUDES' for V1 based on examples.*
    *   `description` (TEXT, nullable, for admin clarity)
    *   `created_at`, `updated_at`
    *   *Alternative/Extension:* Store more complex rules (e.g., depending on multiple selections) using a JSONB field containing a structured rule definition.

*   `pricing_rules` (Representing "If options A & B are selected, price of option C becomes Z")
    *   `id` (PK, UUID/Serial)
    *   `product_type_id` (FK to `product_types`, scope the rule)
    *   `condition_options` (JSONB or TEXT array containing `part_option_id`s that must be selected for the rule to trigger) - Needs indexing if using JSONB.
    *   `target_option_id` (FK to `part_options`, the option whose price is affected)
    *   `new_price` (DECIMAL/NUMERIC, the absolute price to apply)
    *   `priority` (INTEGER, default: 0, to handle conflicting rules - higher priority wins)
    *   `description` (TEXT, nullable, for admin clarity)
    *   `created_at`, `updated_at`
    *   *Alternative:* Instead of `new_price`, could have `price_adjustment` (relative change). `new_price` seems simpler based on the PRD example.

*   `admin_users`
    *   `id` (PK, UUID/Serial)
    *   `username` (VARCHAR, unique)
    *   `password_hash` (VARCHAR)
    *   `created_at`, `updated_at`

*   *(Optional V1 - Cart Persistence):* `cart_sessions` / `cart_items` if server-side session storage isn't sufficient or more structured storage is desired. For V1, leaning towards standard session middleware.

**6. API Design / Contracts**

Using RESTful principles with JSON payloads.

**Customer API:**

*   `GET /products/{productTypeId}/configuration`:
    *   Response: Full structure of part categories and options for the product type, including base prices and stock status.
    *   `200 OK`, Payload: `{ productType: {...}, categories: [{..., options: [{id, name, basePrice, isInStock}]}] }`
*   `POST /products/{productTypeId}/evaluate`:
    *   Request Body: `{ selectedOptions: [optionId1, optionId2, ...] }`
    *   Response: Calculated total price, and for each category, the list of currently available/compatible options and their stock status.
    *   `200 OK`, Payload: `{ totalPrice: 303.00, configuration: { categoryId1: { availableOptions: [optionIdA, optionIdB], unavailableOptions: [{id: optionIdC, reason: 'incompatible'/'out_of_stock'}] }, ... } }`
*   `POST /cart`:
    *   Request Body: `{ productTypeId: ..., selectedOptions: [optionId1, ...], price: 303.00 }`
    *   Response: Updated cart representation (or success status).
    *   `200 OK` or `201 Created`.
*   `GET /cart`:
    *   Response: Current contents of the cart.
    *   `200 OK`, Payload: `{ items: [{ productTypeId: ..., selectedOptions: [...], price: ... }] }`

**Admin API (Requires Authentication - Bearer Token):**

*   `POST /admin/login`:
    *   Request Body: `{ username: "...", password: "..." }`
    *   Response: `200 OK`, Payload: `{ token: "jwt.token.string" }`
*   Standard CRUD endpoints for:
    *   `/admin/product-types` (GET, POST, GET /:id, PUT /:id, DELETE /:id)
    *   `/admin/part-categories`
    *   `/admin/part-options` (Include updating `base_price`, `is_in_stock`)
    *   `/admin/rules/compatibility`
    *   `/admin/rules/pricing`
*   Responses: Standard REST patterns (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `500 Internal Server Error`).

**7. Technology Stack & Rationale**

*   **Frontend:** **React** with **TypeScript**.
    *   *Rationale:* Component-based architecture suits the dynamic UI. Strong community support, good state management libraries (like Redux Toolkit or Zustand), TypeScript enhances maintainability and reduces runtime errors.
*   **Backend:** **Node.js** with **Express.js** and **TypeScript**.
    *   *Rationale:* Efficient for I/O-bound operations (API calls, DB interactions). Non-blocking nature helps with responsiveness. Shared language (TypeScript) with frontend simplifies development potentially. Large ecosystem (NPM).
*   **Database:** **PostgreSQL**.
    *   *Rationale:* Mature, feature-rich open-source RDBMS. Excellent support for JSONB (useful for complex rule conditions), robust, reliable, good performance.
*   **ORM:** **Prisma** or **TypeORM** (for Node.js/TypeScript).
    *   *Rationale:* Provides type safety for database interactions, simplifies query building, manages migrations.
*   **Authentication:** **JWT (JSON Web Tokens)** for Admin API sessions.
    *   *Rationale:* Standard stateless authentication mechanism suitable for APIs.
*   **Caching (Optional but recommended):** **Redis**.
    *   *Rationale:* In-memory data store for caching frequently accessed, rarely changing data like product structures and rules, significantly improving performance of the `/evaluate` endpoint.

**8. Deployment & Infrastructure Considerations**

*   **Containerization:** Dockerize the frontend SPA (served via Nginx/Caddy) and the backend API service.
*   **CI/CD:** Implement a pipeline (e.g., GitHub Actions, GitLab CI, Jenkins) for automated builds, tests, and deployments.
*   **Hosting:** Cloud platform (AWS, GCP, Azure).
    *   Backend API: Container orchestration service (e.g., AWS ECS/EKS, Google Cloud Run/GKE).
    *   Database: Managed database service (e.g., AWS RDS, Google Cloud SQL).
    *   Frontend: Static file hosting (e.g., AWS S3 + CloudFront, Netlify, Vercel).
    *   (Optional) Redis: Managed cache service (e.g., AWS ElastiCache, Google Memorystore).
*   **Environments:** Separate environments for Development, Staging (UAT), and Production.

**9. Security Considerations**

*   **Authentication:** Secure password hashing (e.g., bcrypt) for admin users. JWT implementation using strong secrets and appropriate expiration times. HTTPS required.
*   **Authorization:** Middleware on backend to ensure only authenticated admins can access `/admin/*` endpoints. Implement Role-Based Access Control (RBAC) if roles expand later.
*   **Input Validation:** Rigorous validation on all API inputs (request bodies, query parameters) using libraries like `zod` or `class-validator` to prevent injection attacks (SQLi, NoSQLi) and ensure data integrity.
*   **Cross-Site Scripting (XSS):** Frontend framework (React) provides some protection. Ensure proper escaping of any user-generated content displayed (though minimal in V1 customer UI). Sanitize HTML if rich text is ever introduced. Use appropriate HTTP security headers (CSP, X-Frame-Options, etc.).
*   **Cross-Site Request Forgery (CSRF):** SPAs using token-based auth (JWT in headers) are generally less vulnerable than cookie-based sessions, but ensure no critical state changes via GET requests. Consider standard CSRF protection if using cookies for sessions.
*   **Rate Limiting:** Implement rate limiting on the API, especially the `/evaluate` and `/admin/login` endpoints, to mitigate brute-force and DoS attacks.
*   **Dependency Management:** Use tools like `npm audit` or Snyk to scan for vulnerabilities in third-party libraries. Keep dependencies updated.

**10. Performance & Scalability Considerations**

*   **Performance:**
    *   **Rule Engine:** Optimize rule evaluation logic. Minimize database queries per evaluation request. Pre-fetch/cache rules and product structures associated with a `productTypeId` (use Redis or in-memory cache with clear invalidation strategy on admin updates).
    *   **Database:** Index frequently queried columns (FKs, `product_type_id` in rule tables, potentially JSONB fields used in conditions). Analyze query performance (`EXPLAIN ANALYZE`).
    *   **API:** Ensure backend API is stateless for horizontal scaling. Use efficient serialization/deserialization.
    *   **Frontend:** Code splitting, lazy loading components, optimizing asset delivery (bundling, minification, compression, CDN). Debounce/throttle frequent UI updates triggered by configuration changes if needed.
*   **Scalability:**
    *   **Backend:** Stateless API design allows easy horizontal scaling by adding more instances behind a load balancer.
    *   **Database:** Start with a managed instance; can scale vertically (more resources) or horizontally (read replicas) if needed. Partitioning might be considered if data volume becomes extremely large (unlikely for V1).
    *   **Architecture:** The component-based design and flexible data model facilitate adding new `ProductType`s and their associated rules without major refactoring.

**11. Monitoring, Logging & Alerting**

*   **Logging:** Implement structured logging (JSON format) in the backend API. Log key events (requests, errors, rule evaluation steps, admin actions). Include correlation IDs to trace requests across services.
*   **Monitoring:** Track key application metrics: API request latency (especially `/evaluate`), error rates (HTTP 4xx/5xx), resource utilization (CPU, memory, DB connections), cache hit/miss ratio. Use tools like Prometheus/Grafana, Datadog, or cloud provider's native monitoring.
*   **Alerting:** Configure alerts for critical conditions: high error rates, high latency spikes, resource exhaustion, application crashes, critical rule evaluation failures. Integrate with PagerDuty, Slack, etc.
*   **Health Checks:** Implement `/health` endpoints for load balancers and orchestration services.

**12. Error Handling & Resilience**

*   **API:** Implement consistent error handling middleware. Return standardized JSON error responses with appropriate HTTP status codes and meaningful error messages/codes.
*   **Rule Engine:** Handle cases where rules might conflict or be ill-defined. Log such issues clearly. The system should ideally prevent saving contradictory rules via the admin UI.
*   **Database:** Use connection pooling. Implement retry logic for transient database connection issues. Handle potential constraint violations gracefully.
*   **Frontend:** Display user-friendly error messages for API failures or validation issues. Avoid showing raw technical errors. Provide clear feedback during asynchronous operations (loading states).

**13. Testing Strategy**

*   **Unit Tests:** (.spec.ts files)
    *   Backend: Test individual functions/modules, especially the core logic within the Rule Engine (compatibility checks, price calculations for various scenarios), utility functions, data transformations. Mock dependencies (DB, external services).
    *   Frontend: Test individual components, utility functions, state management logic.
*   **Integration Tests:** (.integration.spec.ts files)
    *   Backend: Test API endpoints by making HTTP requests to a running instance connected to a test database. Verify request/response schemas, status codes, and database side-effects. Focus heavily on the `/evaluate` endpoint with complex configurations and rules. Test auth middleware and admin CRUD operations end-to-end at the API level.
*   **End-to-End (E2E) Tests:** (Using Cypress, Playwright)
    *   Simulate full user journeys in a browser:
        *   Customer: Load product, select various options, see price/compatibility updates, add to cart. Test edge cases with rules.
        *   Admin: Log in, create a new part option, define a compatibility rule, define a pricing rule, update stock, verify changes on the customer UI.
*   **Code Quality:** Linting (ESLint), static analysis, code reviews.

**14. Alternatives Considered**

*   **Database for Rules:** Using a NoSQL database (like MongoDB) specifically for rules for potentially greater schema flexibility. *Rejected for V1* in favor of PostgreSQL's JSONB capabilities to keep the stack simpler and leverage relational integrity for core product data.
*   **Dedicated Rule Engine Library:** Integrating an off-the-shelf rule engine (e.g., `json-rules-engine`, Drools). *Rejected for V1* to avoid adding an external dependency early on; custom implementation deemed feasible initially. Can be revisited if complexity grows significantly.
*   **Backend Language:** Python (Django/Flask), Java (Spring Boot), Go. *Decision:* Node.js/TypeScript chosen for perceived ecosystem benefits and potential synergy with a React frontend, but alternatives are viable.
*   **Server-Side Rendering (SSR):** Using frameworks like Next.js or Nuxt.js. *Rejected for V1* as the highly dynamic nature of the configuration tool lends itself well to an SPA, and V1 doesn't have strong SEO requirements for the configuration page itself.

**15. Open Questions / Risks / Dependencies**

*   **Risk:** Performance of the `evaluate` endpoint under complex rule sets and many concurrent users. *Mitigation:* Aggressive caching, optimized rule evaluation logic, load testing before launch.
*   **Risk:** Complexity of the Admin UI for managing rules becomes unusable for Marcus. *Mitigation:* Iterative UI/UX design involving Marcus's feedback early and often. Provide clear documentation and examples within the UI.
*   **Risk:** Defining conflicting or ambiguous rules (both compatibility and pricing). *Mitigation:* Implement validation checks in the Admin UI/API when saving rules. Establish clear rule priority mechanisms (e.g., `priority` field in `pricing_rules`).
*   **Open Question:** Exact structure/DSL (Domain Specific Language) for storing complex multi-conditional rules in JSONB fields if the simple table structure proves insufficient. Needs further refinement during implementation based on real rule examples.
*   **Open Question:** Specific requirements for session persistence for the cart in V1 (timeout duration?). Assume standard session cookie timeouts initially.
*   **Dependency:** Requires the complete and accurate set of initial parts, options, prices, stock levels, compatibility rules, and pricing rules from Marcus for initial data population and testing.
*   **Dependency:** Finalized UI/UX designs for both customer and admin interfaces.
