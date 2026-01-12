"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { GitPullRequest, ExternalLink, CheckCircle, Clock, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { GithubPR } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002"

function MyPrItem({ pr }: { pr: GithubPR }) {
    const [isExpanded, setIsExpanded] = React.useState(false)

    const getStatusIcon = (pr: GithubPR) => {
        // If mergeable info is not available, default to pending state
        if (!pr.mergeable_state && pr.mergeable === undefined) {
            return (
                <span title="Waiting for approval/checks">
                    <Clock className="h-4 w-4 text-yellow-500" />
                </span>
            )
        }

        if (pr.mergeable_state === "clean" || (pr.mergeable && pr.mergeable_state !== "blocked")) {
            return (
                <span title="Ready to merge">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                </span>
            )
        } else if (pr.mergeable === false) {
            return (
                <span title="Conflicts">
                    <AlertCircle className="h-4 w-4 text-red-500" />
                </span>
            )
        } else {
            // Blocked, drafts, or unstable
            return (
                <span title="Waiting for approval/checks">
                    <Clock className="h-4 w-4 text-yellow-500" />
                </span>
            )
        }
    }

    return (
        <div className="flex w-full items-start gap-2 border-b pb-2 last:border-0 last:pb-0">
            <div
                className="space-y-1 flex-1 min-w-0 cursor-pointer"
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
                    <span className="flex items-center gap-1 text-xs text-muted-foreground">
                        {getStatusIcon(pr)}
                        <span className="capitalize">{pr.mergeable_state?.replace('_', ' ') || 'Open'}</span>
                    </span>
                </div>
                <p className={`text-sm font-medium leading-tight ${isExpanded ? 'whitespace-normal break-words' : 'truncate'}`} title={pr.title}>
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
            <Button variant="ghost" size="icon" className="h-7 w-7 shrink-0" asChild>
                <a href={pr.url || '#'} target="_blank" rel="noopener noreferrer" aria-label="Open PR in GitHub">
                    <ExternalLink className="h-3 w-3" />
                </a>
            </Button>
        </div>
    )
}

export function MyPrsWidget() {
    const [prs, setPrs] = React.useState<GithubPR[]>([])
    const [loading, setLoading] = React.useState(true)

    React.useEffect(() => {
        const fetchPrs = async () => {
            try {
                const res = await fetch(`${API_URL}/api/v1/github/my-prs`)
                if (res.ok) {
                    const data = await res.json()
                    setPrs(data)
                }
            } catch (error) {
                console.error("Failed to fetch My PRs", error)
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
                <CardTitle className="text-sm font-medium">My Pull Requests</CardTitle>
                <GitPullRequest className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent className="flex-1 overflow-hidden">
                <ScrollArea className="h-[200px] w-full">
                    {loading ? (
                        <div className="text-muted-foreground text-sm text-center py-4">Loading...</div>
                    ) : prs.length === 0 ? (
                        <div className="text-muted-foreground text-sm text-center py-4">No open PRs.</div>
                    ) : (
                        <div className="space-y-4">
                            {prs.map((pr, index) => (
                                <MyPrItem key={index} pr={pr} />
                            ))}
                        </div>
                    )}
                </ScrollArea>
            </CardContent>
        </Card>
    )
}
