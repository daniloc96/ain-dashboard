"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckSquare, ExternalLink, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { JiraIssue } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002"

export function JiraTasksWidget() {
    const [tasks, setTasks] = React.useState<JiraIssue[]>([])
    const [loading, setLoading] = React.useState(true)
    const [expanded, setExpanded] = React.useState<Record<string, boolean>>({})

    React.useEffect(() => {
        const fetchTasks = async () => {
            try {
                const res = await fetch(`${API_URL}/api/v1/jira/tasks`)
                if (res.ok) {
                    const data = await res.json()
                    setTasks(data)
                }
            } catch (error) {
                console.error("Failed to fetch Jira tasks", error)
            } finally {
                setLoading(false)
            }
        }
        fetchTasks()

        // Auto-refresh every 5 minutes
        const interval = setInterval(fetchTasks, 5 * 60 * 1000)
        return () => clearInterval(interval)
    }, [])

    const getStatusColor = (status: string) => {
        const s = status.toLowerCase();
        if (s.includes('progress')) return "bg-blue-500/10 text-blue-500 hover:bg-blue-500/20";
        if (s.includes('done') || s.includes('complete')) return "bg-green-500/10 text-green-500 hover:bg-green-500/20";
        if (s.includes('blocked')) return "bg-red-500/10 text-red-500 hover:bg-red-500/20";
        return "bg-secondary text-secondary-foreground hover:bg-secondary/80";
    }

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">My Tasks</CardTitle>
                <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent className="flex-1 overflow-hidden">
                <ScrollArea className="h-[240px] w-full pr-2">
                    {loading ? (
                        <div className="text-muted-foreground text-sm text-center py-4">Loading...</div>
                    ) : tasks.length === 0 ? (
                        <div className="text-muted-foreground text-sm text-center py-4">No active tasks.</div>
                    ) : (
                        <div className="space-y-3">
                            {tasks.map((task) => (
                                <div key={task.key} className="flex w-full items-start gap-2 border-b pb-2 last:border-0 last:pb-0">
                                    <div
                                        className="flex-1 min-w-0 space-y-1 cursor-pointer"
                                        role="button"
                                        tabIndex={0}
                                        aria-expanded={!!expanded[task.key]}
                                        onClick={() => setExpanded(prev => ({ ...prev, [task.key]: !prev[task.key] }))}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter' || e.key === ' ') {
                                                e.preventDefault()
                                                setExpanded(prev => ({ ...prev, [task.key]: !prev[task.key] }))
                                            }
                                        }}
                                    >
                                        <div className="flex items-center gap-2 flex-wrap">
                                            <span className="text-xs font-mono text-muted-foreground shrink-0">{task.key}</span>
                                            <Badge variant="secondary" className={`text-[10px] px-1.5 py-0 shrink-0 ${getStatusColor(task.status)}`}>
                                                {task.status}
                                            </Badge>
                                        </div>
                                        <p className={`text-sm font-medium leading-tight ${expanded[task.key] ? 'whitespace-normal break-words' : 'truncate'}`} title={task.summary}>
                                            {task.summary}
                                        </p>
                                    </div>
                                    <Button variant="ghost" size="icon" className="h-7 w-7 shrink-0" asChild>
                                        <a href={task.url} target="_blank" rel="noopener noreferrer" title="Open in Jira">
                                            <ExternalLink className="h-4 w-4" />
                                        </a>
                                    </Button>
                                </div>
                            ))}
                        </div>
                    )}
                </ScrollArea>
            </CardContent>
        </Card>
    )
}
