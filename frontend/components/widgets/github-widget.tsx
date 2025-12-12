"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { GitPullRequest, ExternalLink, GitMerge, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { GithubPR } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export function GithubWidget() {
    const [prs, setPrs] = React.useState<GithubPR[]>([])
    const [loading, setLoading] = React.useState(true)

    React.useEffect(() => {
        const fetchPrs = async () => {
            try {
                const res = await fetch(`${API_URL}/api/v1/github/prs`)
                if (res.ok) {
                    const data = await res.json()
                    setPrs(data)
                }
            } catch (error) {
                console.error("Failed to fetch PRs", error)
            } finally {
                setLoading(false)
            }
        }
        fetchPrs()

        // Auto-refresh every 5 minutes
        const interval = setInterval(fetchPrs, 5 * 60 * 1000)
        return () => clearInterval(interval)
    }, [])

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Pull Requests Review</CardTitle>
                <GitPullRequest className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent className="flex-1 overflow-hidden">
                <ScrollArea className="h-[200px] w-full pr-4">
                    {loading ? (
                        <div className="text-muted-foreground text-sm text-center py-4">Loading...</div>
                    ) : prs.length === 0 ? (
                        <div className="text-muted-foreground text-sm text-center py-4">No pending reviews.</div>
                    ) : (
                        <div className="space-y-4">
                            {prs.map((pr, index) => (
                                <div key={index} className="flex items-start justify-between space-x-2 border-b pb-2 last:border-0 last:pb-0">
                                    <div className="space-y-1">
                                        <div className="flex items-center gap-2">
                                            <Badge variant="outline" className="text-xs">{pr.repo}</Badge>
                                            <span className="text-xs text-muted-foreground">by {pr.author}</span>
                                        </div>
                                        <p className="text-sm font-medium leading-none truncate max-w-[200px] sm:max-w-[300px]" title={pr.title}>
                                            {pr.title}
                                        </p>
                                    </div>
                                    <Button variant="ghost" size="icon" className="h-6 w-6" asChild>
                                        <a href={pr.url} target="_blank" rel="noopener noreferrer">
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
