"use client"

import * as React from "react"
import { Mail, SquareKanban } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002"

export function QuickLinksBar() {
    const [unreadCount, setUnreadCount] = React.useState<number>(0)
    const [loading, setLoading] = React.useState(true)

    React.useEffect(() => {
        const fetchUnreadCount = async () => {
            try {
                const res = await fetch(`${API_URL}/api/v1/gmail/unread`)
                if (res.ok) {
                    const data = await res.json()
                    setUnreadCount(data.count)
                }
            } catch (error) {
                console.error("Failed to fetch Gmail unread count", error)
            } finally {
                setLoading(false)
            }
        }

        fetchUnreadCount()

        // Auto-refresh every 5 minutes
        const interval = setInterval(fetchUnreadCount, 5 * 60 * 1000)
        return () => clearInterval(interval)
    }, [])

    const openGmail = () => {
        window.open("https://mail.google.com", "_blank")
    }

    const [jiraLinks, setJiraLinks] = React.useState<{ name: string; url: string }[]>([])

    React.useEffect(() => {
        // Parse Jira links from environment variable
        // Format: JSON string or just empty
        const linksEnv = process.env.NEXT_PUBLIC_JIRA_LINKS
        if (linksEnv) {
            try {
                const parsed = JSON.parse(linksEnv)
                if (Array.isArray(parsed)) {
                    setJiraLinks(parsed)
                }
            } catch (e) {
                console.error("Failed to parse NEXT_PUBLIC_JIRA_LINKS", e)
            }
        }
    }, [])

    return (
        <div className="flex items-center gap-2">
            {/* Dynamic Jira Links */}
            {jiraLinks.map((link, i) => (
                <Button
                    key={i}
                    variant="outline"
                    size="sm"
                    className="h-9 gap-2 px-3 border-muted-foreground/30 hover:border-muted-foreground/50"
                    onClick={() => window.open(link.url, "_blank")}
                    title={link.name}
                >
                    <SquareKanban className="h-4 w-4" />
                    <span className="hidden sm:inline-block font-medium">{link.name}</span>
                </Button>
            ))}

            {/* Gmail Icon with Badge */}
            <Button
                variant="outline"
                size="icon"
                className="relative h-9 w-9 border-muted-foreground/30 hover:border-muted-foreground/50"
                onClick={openGmail}
                title="Open Gmail"
            >
                <Mail className="h-4 w-4" />
                {!loading && unreadCount > 0 && (
                    <Badge
                        className="absolute -top-1 -right-1 h-5 min-w-[20px] px-1 flex items-center justify-center text-[10px] bg-red-500 hover:bg-red-500 text-white"
                    >
                        {unreadCount > 99 ? "99+" : unreadCount}
                    </Badge>
                )}
            </Button>
        </div>
    )
}
