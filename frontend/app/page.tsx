"use client"

import { TodoWidget } from "@/components/widgets/todo-widget"
import { GithubWidget } from "@/components/widgets/github-widget"
import { MyPrsWidget } from "@/components/widgets/my-prs-widget"
import { JiraTasksWidget } from "@/components/widgets/jira-tasks-widget"
import { CalendarWidget } from "@/components/widgets/calendar-widget"
import { GoogleAuthDialog } from "@/components/google-auth-dialog"
import { useGoogleAuthStatus } from "@/hooks/use-google-auth-status"
import * as React from "react"

export default function DashboardPage() {
  const { authStatus, isLoading, error } = useGoogleAuthStatus()
  const [showAuthDialog, setShowAuthDialog] = React.useState(false)

  React.useEffect(() => {
    // Show dialog if Google auth is expired or not configured
    if (authStatus && authStatus.status !== "authorized") {
      setShowAuthDialog(true)
    }
  }, [authStatus])

  return (
    <>
      {authStatus && authStatus.status !== "authorized" && (
        <GoogleAuthDialog
          open={showAuthDialog}
          onOpenChange={setShowAuthDialog}
          status={authStatus.status as "expired" | "not_configured"}
          authUrl={authStatus.auth_url}
        />
      )}

      <div className="flex flex-col gap-3 p-3 sm:p-4 min-h-screen">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">

          {/* Row 1 */}
          <div className="col-span-1 border rounded-xl overflow-hidden shadow-sm bg-card/50 min-h-[280px] sm:min-h-[320px]">
            <TodoWidget />
          </div>
          <div className="col-span-1 border rounded-xl overflow-hidden shadow-sm bg-card/50 min-h-[280px] sm:min-h-[320px]">
            <CalendarWidget />
          </div>

          {/* Row 2 */}
          <div className="col-span-1 border rounded-xl overflow-hidden shadow-sm bg-card/50 min-h-[280px] sm:min-h-[320px]">
            <JiraTasksWidget />
          </div>
          <div className="col-span-1 border rounded-xl overflow-hidden shadow-sm bg-card/50 min-h-[280px] sm:min-h-[320px]">
            <GithubWidget />
          </div>

          {/* Row 3 */}
          <div className="col-span-1 border rounded-xl overflow-hidden shadow-sm bg-card/50 min-h-[280px] sm:min-h-[320px]">
            <MyPrsWidget />
          </div>

        </div>
      </div>
    </>
  )
}
