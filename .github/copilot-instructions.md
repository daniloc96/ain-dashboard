# AIN Dashboard - AI Coding Agent Instructions

## Architecture Overview

This is a **local-first personal productivity dashboard** that aggregates work streams into a single UI:
- **Frontend**: Next.js 16 (App Router) + TypeScript + Tailwind CSS + shadcn/ui components
- **Backend**: FastAPI (Python) + SQLAlchemy + PostgreSQL
- **Deployment**: Docker Compose orchestrates all services (frontend:3001, backend:8001, postgres:5433)
- **External Integrations**: GitHub, Jira (multi-domain), Google Calendar, Gmail via API tokens/OAuth

## Critical Developer Workflows

### Starting the Stack
```bash
docker compose up -d                    # Start all services
docker compose logs -f backend          # View backend logs
docker compose logs -f frontend         # View frontend logs
docker compose down                     # Stop all services
```

### Backend Development
- **No hot reload**: Backend requires rebuild after code changes (`docker compose restart backend`)
- **DB connection retry logic**: [main.py](backend/main.py) has 5-attempt retry on startup - essential for Docker compose startup race conditions
- **API docs**: http://localhost:8001/docs (FastAPI auto-generated Swagger UI)

### Frontend Development
- **Uses React 19 + Next.js 16** with experimental features (React Compiler enabled in [package.json](frontend/package.json))
- **Client-side only**: All widgets use `"use client"` directive - no SSR for these interactive components
- **Auto-refresh pattern**: Widgets use [use-auto-refresh.ts](frontend/hooks/use-auto-refresh.ts) hook (5-min interval by default)

## Project-Specific Patterns

### Multi-Domain Jira Support
[services/jira_service.py](backend/services/jira_service.py) supports **comma-separated** `JIRA_DOMAINS` env var:
```python
JIRA_DOMAINS = "company1.atlassian.net,company2.atlassian.net"
```
JQL queries are **executed per-domain** and aggregated into a single response list.

### GitHub Team Review Discovery
[services/github_service.py](backend/services/github_service.py) has **startup caching** of user teams (`_user_teams_cache`):
- Fetches user's GitHub organizations + teams **once at container start**
- Queries both personal review requests (`review-requested:@me`) AND team requests (`team-review-requested:org/team`)
- Results are **deduplicated by URL** using a dict to prevent duplicate PRs in UI

### Google OAuth Shared Credentials
[services/google_auth.py](backend/services/google_auth.py) provides `get_credentials()` for **both Calendar and Gmail**:
- Single `token.json` + `credentials.json` pair (mounted via Docker volume in [docker-compose.yml](docker-compose.yml))
- OAuth scopes: `calendar.readonly` and `gmail.readonly`
- Automatic refresh logic with fallback to `run_local_server()` if token expired

### Database CRUD Conventions
[crud.py](backend/crud.py) uses an **order field** for drag-and-drop support:
- `create_todo()`: Sets `order = max(order) + 1`
- `reorder_todos()`: Bulk updates order field based on ID list from frontend
- All queries: `.order_by(models.Todo.order)` for consistent display order

### Widget Component Structure
All widgets in [components/widgets/](frontend/components/widgets/) follow this pattern:
```tsx
// 1. Use "use client" directive
// 2. Import useAutoRefresh hook
// 3. Define API fetch function (async)
// 4. Render Card with loading/error states
// 5. Map data to UI elements
```
Example: [todo-widget.tsx](frontend/components/widgets/todo-widget.tsx) uses `@dnd-kit` for drag-and-drop with `SortableContext`.

## Key Integration Details

### FastAPI Router Registration
[main.py](backend/main.py) uses `app.include_router()` for modular endpoints:
- All routers in [routers/](backend/routers/) use `/api/v1/{resource}` prefix pattern
- Services layer ([services/](backend/services/)) handles external API calls
- Routers stay thin - just request validation and response marshalling

### Environment Variables Flow
1. Root `.env` file (not in repo - copy from `.env.example`)
2. Docker Compose passes vars to containers via `environment:` blocks
3. Backend: `os.getenv()` with defaults
4. Frontend: `NEXT_PUBLIC_*` prefix required for client-side access (e.g., `NEXT_PUBLIC_API_URL`)

### CORS Configuration
[main.py](backend/main.py) uses `allow_origins=["*"]` for **local dev friction reduction** - should be restricted in production deployments.

## Common Gotchas

1. **Backend volume mounting**: [docker-compose.yml](docker-compose.yml) mounts `./backend:/app` for live code updates but **SQLAlchemy models require container restart** to pick up schema changes
2. **Frontend build args**: `NEXT_PUBLIC_*` vars must be passed as Docker build args AND runtime environment in [docker-compose.yml](docker-compose.yml)
3. **PostgreSQL port**: Exposed on `5433` (not default 5432) to avoid conflicts with local Postgres installations
4. **Jira status filter**: `JIRA_TASK_STATUS_ENABLED` env var is comma-separated - defaults to `"In Progress"` if not set
5. **shadcn/ui components**: Generated in [components/ui/](frontend/components/ui/) - don't hand-edit, use `npx shadcn@latest add <component>`
