// Types matching backend schemas

export interface Todo {
    id: number;
    title: string;
    completed: boolean;
    order: number;
}

export interface GithubPR {
    title: string;
    url: string;
    repo: string;
    author: string;
    created_at: string;
    state: string;
}

export interface JiraIssue {
    key: string;
    summary: string;
    status: string;
    priority: string;
    assignee: string;
    url: string;
}

export interface CalendarEvent {
    summary: string;
    start_time: string;
    end_time: string;
    location?: string;
    html_link: string;
}
