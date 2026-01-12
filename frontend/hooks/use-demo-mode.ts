"use client"

import { useState, useEffect } from "react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002"

export function useDemoMode() {
  const [isDemoMode, setIsDemoMode] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const checkDemoMode = async () => {
      try {
        const response = await fetch(`${API_URL}/api/v1/demo-mode`)
        if (response.ok) {
          const data = await response.json()
          setIsDemoMode(data.demo_mode)
        }
      } catch (error) {
        console.error("Failed to check demo mode:", error)
      } finally {
        setIsLoading(false)
      }
    }

    checkDemoMode()
  }, [])

  return { isDemoMode, isLoading }
}
