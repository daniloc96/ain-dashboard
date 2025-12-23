"use client"

import { useDemoMode } from "@/hooks/use-demo-mode"
import { Badge } from "@/components/ui/badge"
import { FlaskConical } from "lucide-react"

export function DemoModeBanner() {
  const { isDemoMode, isLoading } = useDemoMode()

  if (isLoading || !isDemoMode) {
    return null
  }

  return (
    <div className="fixed top-2 right-2 z-50">
      <Badge 
        variant="outline" 
        className="bg-amber-500/10 text-amber-500 border-amber-500/30 gap-1.5 px-3 py-1.5 text-sm font-medium"
      >
        <FlaskConical className="h-4 w-4" />
        Demo Mode
      </Badge>
    </div>
  )
}
