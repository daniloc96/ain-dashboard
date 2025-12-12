"use client"

import * as React from "react"
import { Mail } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

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

    return (
        <div className="flex items-center gap-2">
            {/* Gmail Icon with Badge */}
            <Button
                variant="ghost"
                size="icon"
                className="relative h-9 w-9"
                onClick={openGmail}
                title="Open Gmail"
            >
                <Mail className="h-5 w-5" />
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
