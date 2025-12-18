"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Calendar, MapPin, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { CalendarEvent } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

function CalendarEventItem({ event, formatTime }: { event: CalendarEvent, formatTime: (iso: string) => string }) {
  const [isExpanded, setIsExpanded] = React.useState(false)

  return (
    <div className="flex w-full items-start justify-between space-x-2 border-b pb-2 last:border-0 last:pb-0">
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
          <span className="text-xs font-semibold text-primary">
            {formatTime(event.start_time)} - {formatTime(event.end_time)}
          </span>
        </div>
        <p className={`text-sm font-medium leading-none ${isExpanded ? 'whitespace-normal break-words' : 'truncate'} max-w-[200px]`} title={event.summary}>
          {event.summary}
        </p>
        {event.location && (
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <MapPin className="h-3 w-3" />
            <span className={isExpanded ? 'whitespace-normal break-words' : 'truncate max-w-[150px]'}>{event.location}</span>
          </div>
        )}
      </div>
      <Button variant="ghost" size="icon" className="h-6 w-6 shrink-0" asChild>
        <a href={event.html_link} target="_blank" rel="noopener noreferrer" aria-label="Open calendar event">
          <ExternalLink className="h-3 w-3" />
        </a>
      </Button>
    </div>
  )
}

export function CalendarWidget() {
  const [events, setEvents] = React.useState<CalendarEvent[]>([])
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    const fetchEvents = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/calendar/events`)
        if (res.ok) {
          const data = await res.json()
          setEvents(data)
        }
      } catch (error) {
        console.error("Failed to fetch calendar events", error)
      } finally {
        setLoading(false)
      }
    }
    fetchEvents()

    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchEvents, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">Today's Events</CardTitle>
        <Calendar className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden">
        <ScrollArea className="h-[200px] w-full pr-4">
          {loading ? (
            <div className="text-muted-foreground text-sm text-center py-4">Loading...</div>
          ) : events.length === 0 ? (
            <div className="text-muted-foreground text-sm text-center py-4">No events today.</div>
          ) : (
            <div className="space-y-4">
              {events.map((event, index) => (
                <CalendarEventItem key={index} event={event} formatTime={formatTime} />
              ))}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
