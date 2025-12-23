# 🚀 AIN Dashboard

> **Your All-In-One Personal Command Center.**  
> Don't lose your mind—organize your work day in one beautiful, darkness-themed interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/frontend-Next.js_16-black)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-teal)
![Docker](https://img.shields.io/badge/deployment-Docker-blue)

**AIN Dashboard** is a local-first, privacy-focused productivity dashboard designed for developers. It aggregates your critical work streams—Jira tickets, GitHub PRs, Calendar events, and Todos—into a single, highly customizable view.

---

## ✨ Features

*   **🎨 Application-Like UI**: Built with a sleek, dark-grey aesthetic that reduces eye strain.
*   **🧩 Modular Widget System**:
    *   **📝 Todo List**: Rapid-fire task management with persistence.
    *   **🐙 GitHub Widget**: Track Pull Requests requiring your review in real-time.
    *   **🎫 Jira Widget**: View your tasks filtered by configurable statuses across multiple Jira instances.
    *   **📅 Calendar**: See your daily schedule at a glance.
*   **🏗️ Full-Stack Architecture**:
    *   **Frontend**: Next.js 16, TailwindCSS, Shadcn/UI, Lucide Icons.
    *   **Backend**: FastAPI (Python), SQLModel.
    *   **Database**: PostgreSQL (Dockerized with persistent volumes).
*   **🐳 Dockerized**: One command to spin up the entire stack.

---

## 🛠️ Tech Stack

*   **Frontend**: [Next.js](https://nextjs.org/) (App Router), [TypeScript](https://www.typescriptlang.org/), [Tailwind CSS](https://tailwindcss.com/)
*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/)
*   **Database**: [PostgreSQL](https://www.postgresql.org/)
*   **Infrastructure**: [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started

### Prerequisites

*   [Docker](https://www.docker.com/) and Docker Compose installed on your machine.
*   Git.

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/ain-dashboard.git
    cd ain-dashboard
    ```

2.  **Configure Environment**
    Copy the example environment file to a real `.env` file:
    ```bash
    cp .env.example .env
    ```

3.  **Start the Application**
    Run the entire stack with Docker Compose:
    ```bash
    docker compose up -d
    ```

    *   **Frontend**: [http://localhost:3001](http://localhost:3001)
    *   **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

---

## 🔑 Configuration Guide

To unlock the full power of the widgets, you'll need to provide API tokens in your `.env` file.

### 🐙 GitHub Widget

The GitHub widget shows **Pull Requests where your review has been requested** – both personal and team requests.

#### How It Works

*   **Personal reviews**: PRs where you are directly requested as a reviewer
*   **Team reviews**: PRs where any of your GitHub teams are requested as reviewers
*   Teams are **automatically discovered** at container startup (no configuration needed)
*   Results are deduplicated and sorted by date (most recent first)

#### Step 1: Generate a Token

1.  Go to **[GitHub Settings > Developer settings > Personal Access Tokens > Tokens (classic)](https://github.com/settings/tokens)**
2.  Click **"Generate new token (classic)"**
3.  Configure the token:
    *   **Note**: `AIN Dashboard`
    *   **Expiration**: Choose your preference
    *   **Scopes**: Select **`repo`** and **`read:org`** (required for team discovery)
4.  Click **"Generate token"** and copy it immediately

#### Step 2: Authorize for Organizations (SSO) ⚠️ IMPORTANT

If you work with **private repositories in an organization** (e.g., your company's GitHub), you **must authorize the token for SSO**:

1.  After creating the token, go back to [your tokens list](https://github.com/settings/tokens)
2.  Find your new token and look for **"Configure SSO"** button next to it
3.  Click it and then **"Authorize"** for each organization you need access to
4.  If the button says "SSO enabled" with a green checkmark, you're done!

> **🚨 Without this step, the token will NOT have access to private organization repositories, and the widget will show "No pending reviews" even if you have PRs assigned.**

#### Step 3: Add to `.env`

```bash
GITHUB_TOKEN=ghp_your_token_here
```

---

### 🎫 Jira Widget

The Jira widget shows **tasks assigned to you**, filtered by configurable statuses.

#### Step 1: Generate an API Token

1.  Go to **[Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)**
2.  Click **"Create API token"**
3.  Give it a label (e.g., "AIN Dashboard") and copy the generated token

> **Note**: Use a standard API token, NOT an OAuth app credential.

#### Step 2: Configure Multiple Jira Instances (Optional)

AIN Dashboard supports **multiple Jira domains** with the same token (if they belong to the same Atlassian organization):

```bash
# Single domain
JIRA_DOMAINS=yourcompany.atlassian.net

# Multiple domains (comma-separated)
JIRA_DOMAINS=company1.atlassian.net,company2.atlassian.net
```

#### Step 3: Configure Task Filters

Define which task statuses should appear in the widget:

```bash
JIRA_TASK_STATUS_ENABLED="In Progress,To Do,Blocked,Waiting"
```

> **Tip**: Status names are case-sensitive and should match exactly what you see in Jira.

#### Full Jira Configuration

```bash
JIRA_DOMAINS=yourcompany.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your_api_token_here
JIRA_TASK_STATUS_ENABLED="In Progress,To Do"
```

#### Step 4: Configure Quick Links (Optional)

You can add shortcuts to specific Jira boards in the header using a JSON string:

```bash
NEXT_PUBLIC_JIRA_LINKS='[
  {"name": "Sprint Board", "url": "https://your-domain.atlassian.net/jira/software/c/projects/PROJ/boards/1"},
  {"name": "Backlog", "url": "https://your-domain.atlassian.net/jira/software/c/projects/PROJ/boards/1/backlog"}
]'
```

---

### 📅 Google Calendar & Gmail Widgets

The Calendar widget shows **today's events** and the Gmail icon shows **unread email count**. Both support personal and work (Google Workspace) accounts.

#### Step 1: Create a Google Cloud Project

1.  Go to **[Google Cloud Console](https://console.cloud.google.com/)**
2.  Create a **new project** (e.g., "AIN Dashboard")
    *   You can use a personal Google account to avoid creating resources in your company's GCP
3.  Go to **APIs & Services > Library**
4.  Enable the following APIs:
    *   **Google Calendar API** – for calendar events
    *   **Gmail API** – for unread email count

> **⚠️ IMPORTANT**: You MUST enable BOTH APIs! Without this step, you'll get a `403 accessNotConfigured` error. After enabling, wait 1-2 minutes for them to propagate.

#### Step 2: Create OAuth Credentials

1.  Go to **APIs & Services > Credentials**
2.  Click **"Configure Consent Screen"**:
    *   Choose **"External"** user type (or "Internal" if using Google Workspace)
    *   Fill in the required fields (App name, User support email, Developer email)
    *   Add scope: `https://www.googleapis.com/auth/calendar.readonly`
    *   Add your email as a test user
    *   Save and continue
3.  Go back to **Credentials** and click **"Create Credentials" > "OAuth client ID"**:
    *   Application type: **Desktop app**
    *   Name: `AIN Dashboard`
4.  Click **Download JSON** and rename the file to `credentials.json`

#### Step 3: Place the Credentials File

1.  Move `credentials.json` to the `backend/` directory:
    ```bash
    mv ~/Downloads/credentials.json ./backend/credentials.json
    ```

#### Step 4: Authorize Your Account

1.  Start the application:
    ```bash
    docker compose up
    ```
2.  **First time only**: A pop-up dialog will appear in the dashboard asking you to authorize
3.  Click **"Authorize Google Account"** button in the dialog
4.  **Choose the account** you want to use (personal or work email)
5.  Grant permission to read your calendar and email
6.  A `token.json` file will be created automatically, storing your authorization
7.  The dialog will close automatically and the widgets will start working

#### Token Expiration & Renewal

When your Google token expires, the dashboard will automatically detect this and show a pop-up dialog with a link to re-authorize. You can:

*   Click **"Authorize Google Account"** to open the authorization page in a new browser tab
*   After authorizing, click **"Refresh Page"** to reload the dashboard with the new token

> **🔒 Security Note**: The `token.json` file contains your OAuth tokens. It's already in `.gitignore` to prevent accidental commits.

#### Troubleshooting

*   **"Authorization required" dialog appears**: Your token has expired. Simply click the authorization button in the pop-up and follow the steps
*   **"Access blocked" error**: Make sure you added your email as a "Test user" in the OAuth consent screen
*   **Wrong calendar showing**: The widget uses your "primary" calendar. Switch accounts by deleting `backend/token.json` and reauthorizing
*   **Dialog won't close**: Check that you have `NEXT_PUBLIC_API_URL` properly configured pointing to your backend

---

## 📋 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL (default: `http://localhost:8000`) |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `GITHUB_TOKEN` | No | GitHub Personal Access Token with `repo` scope |
| `JIRA_DOMAINS` | No | Comma-separated list of Jira domains |
| `JIRA_EMAIL` | No | Your Atlassian account email |
| `JIRA_API_TOKEN` | No | Atlassian API token |
| `JIRA_TASK_STATUS_ENABLED` | No | Comma-separated list of task statuses to show |
| `POSTGRES_USER` | Yes | PostgreSQL username |
| `POSTGRES_PASSWORD` | Yes | PostgreSQL password |
| `POSTGRES_DB` | Yes | PostgreSQL database name |

---

## 🤝 Contributing

We love open source! Contributions are welcome.

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
