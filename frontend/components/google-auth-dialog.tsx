"use client"

import * as React from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ExternalLink, AlertCircle, X } from "lucide-react"

interface GoogleAuthDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  status: "expired" | "not_configured"
  authUrl: string | null
}

export function GoogleAuthDialog({
  open,
  onOpenChange,
  status,
  authUrl,
}: GoogleAuthDialogProps) {
  const isExpired = status === "expired"

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-yellow-500 shrink-0" />
              <div>
                <CardTitle>
                  {isExpired ? "Google Authorization Expired" : "Google Not Configured"}
                </CardTitle>
              </div>
            </div>
            <button
              onClick={() => onOpenChange(false)}
              className="text-muted-foreground hover:text-foreground"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
          <CardDescription className="mt-2">
            {isExpired
              ? "Your Google authorization token has expired. Please re-authorize to continue using Calendar and Gmail widgets."
              : "Google is not configured yet. Please authorize to enable Calendar and Gmail widgets."}
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          {authUrl && (
            <>
              <p className="text-sm text-muted-foreground">
                Click the button below to open Google's authorization page:
              </p>
              <Button
                onClick={() => window.open(authUrl, "_blank")}
                className="w-full gap-2"
              >
                <ExternalLink className="h-4 w-4" />
                Authorize Google Account
              </Button>
              <p className="text-xs text-muted-foreground">
                After authorizing, the widgets will automatically refresh.
              </p>
            </>
          )}
          {!authUrl && (
            <p className="text-sm text-destructive">
              Unable to generate authorization URL. Please check your Google credentials configuration.
            </p>
          )}

          <div className="flex gap-2 pt-4 border-t">
            <Button
              variant="outline"
              onClick={() => onOpenChange(false)}
              className="flex-1"
            >
              Dismiss
            </Button>
            <Button
              variant="default"
              onClick={() => window.location.reload()}
              className="flex-1"
            >
              Refresh Page
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
