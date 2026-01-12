import { useEffect, useState } from "react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002"

export interface GoogleAuthStatus {
  status: "authorized" | "expired" | "not_configured"
  message: string
  auth_url: string | null
}

export function useGoogleAuthStatus() {
  const [authStatus, setAuthStatus] = useState<GoogleAuthStatus | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const checkAuthStatus = async () => {
    try {
      const url = `${API_URL}/api/v1/google/auth-status`

      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      })

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`)
      }

      const data = await res.json()
      setAuthStatus(data)
      setError(null)
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error)
      setError(errorMsg)
      setAuthStatus(null)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    checkAuthStatus()
    // Check every 5 minutes
    const interval = setInterval(checkAuthStatus, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  return { authStatus, isLoading, error }
}
