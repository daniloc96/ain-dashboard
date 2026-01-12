"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { GitPullRequest, ExternalLink, GitMerge, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { GithubPR } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002"

function GithubPrItem({ pr }: { pr: GithubPR }) {
    const [isExpanded, setIsExpanded] = React.useState(false)

    return (
        <div className="flex w-full items-start gap-2 border-b pb-2 last:border-0 last:pb-0">
            <div
                className="flex-1 min-w-0 space-y-1 cursor-pointer"
                role="button"
                tabIndex={0}
                aria-expanded={isExpanded}
                onClick={() => setIsExpanded(!isExpanded)}
                onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault()
                        setIsExpanded(!isExpanded)
                    }
                }}
            >
                <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-xs">{pr.repo}</Badge>
                    <span className="text-xs text-muted-foreground">by {pr.author}</span>
                </div>
                <p className={`text-sm font-medium leading-none ${isExpanded ? 'whitespace-normal break-words' : 'truncate'} max-w-[200px] sm:max-w-[300px]`} title={pr.title}>
                    {pr.title}
                </p>
                {pr.labels && pr.labels.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-1">
                        {pr.labels.map((label, i) => (
                            <Badge
                                key={i}
                                variant="secondary"
                                className="px-1.5 py-0 text-[10px] h-5 font-normal border-0"
                                style={{
                                    backgroundColor: `#${label.color}`,
                                    color: ((parseInt(label.color.substring(0, 2), 16) * 299 + parseInt(label.color.substring(2, 4), 16) * 587 + parseInt(label.color.substring(4, 6), 16) * 114) / 1000) >= 128 ? 'black' : 'white'
                                }}
                            >
                                {label.name}
                            </Badge>
                        ))}
                    </div>
                )}
            </div>
            <Button variant="ghost" size="icon" className="h-6 w-6 shrink-0" asChild>
                <a href={pr.url} target="_blank" rel="noopener noreferrer" aria-label="Open pull request">
                    <ExternalLink className="h-3 w-3" />
                </a>
            </Button>
        </div>
    )
}

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
                                <GithubPrItem key={index} pr={pr} />
                            ))}
                        </div>
                    )}
                </ScrollArea>
            </CardContent>
        </Card>
    )
}
