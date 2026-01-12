"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Hash, ExternalLink, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { JiraIssue } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002"

export function JiraNotificationsWidget() {
    const [issues, setIssues] = React.useState<JiraIssue[]>([])
    const [loading, setLoading] = React.useState(true)

    React.useEffect(() => {
        const fetchIssues = async () => {
            try {
                const res = await fetch(`${API_URL}/api/v1/jira/notifications`)
                if (res.ok) {
                    const data = await res.json()
                    setIssues(data)
                }
            } catch (error) {
                console.error("Failed to fetch Jira notifications", error)
            } finally {
                setLoading(false)
            }
        }
        fetchIssues()
    }, [])

    const getPriorityColor = (priority: string) => {
        switch (priority.toLowerCase()) {
            case 'highest':
            case 'high':
            case 'critical':
                return "text-red-500 border-red-500/50"
            case 'medium':
                return "text-yellow-500 border-yellow-500/50"
            default:
                return "text-muted-foreground border-border"
        }
    }

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Jira Notifications</CardTitle>
                <Hash className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent className="flex-1 overflow-hidden">
                <ScrollArea className="h-[200px] w-full pr-4">
                    {loading ? (
                        <div className="text-muted-foreground text-sm text-center py-4">Loading...</div>
                    ) : issues.length === 0 ? (
                        <div className="text-muted-foreground text-sm text-center py-4">No recent mentions or watched updates.</div>
                    ) : (
                        <div className="space-y-4">
                            {issues.map((issue) => (
                                <div key={issue.key} className="flex items-start justify-between space-x-2 border-b pb-2 last:border-0 last:pb-0">
                                    <div className="space-y-1">
                                        <div className="flex items-center gap-2">
                                            <Badge variant="outline" className={`text-xs ${getPriorityColor(issue.priority)}`}>{issue.key}</Badge>
                                            <span className="text-xs text-muted-foreground">{issue.status}</span>
                                        </div>
                                        <p className="text-sm font-medium leading-none truncate max-w-[200px] sm:max-w-[300px]" title={issue.summary}>
                                            {issue.summary}
                                        </p>
                                    </div>
                                    <Button variant="outline" size="sm" className="h-6 gap-1" asChild>
                                        <a href={issue.url} target="_blank" rel="noopener noreferrer">
                                            <span className="text-[10px]">Open</span>
                                            <ExternalLink className="h-3 w-3" />
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
