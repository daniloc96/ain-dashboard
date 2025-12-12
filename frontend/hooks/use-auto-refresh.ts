"use client"

import { useState, useEffect, useCallback } from "react"

const REFRESH_INTERVAL = 5 * 60 * 1000 // 5 minutes in milliseconds

/**
 * Custom hook for auto-refreshing data at a fixed interval.
 * @param fetchFn - The function to call to fetch data
 * @param dependencies - Array of dependencies (passed to useCallback)
 * @returns { data, loading, error, refetch, lastUpdated }
 */
export function useAutoRefresh<T>(
    fetchFn: () => Promise<T>,
    initialData: T
) {
    const [data, setData] = useState<T>(initialData)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [lastUpdated, setLastUpdated] = useState<Date | null>(null)

    const refetch = useCallback(async () => {
        try {
            const result = await fetchFn()
            setData(result)
            setError(null)
            setLastUpdated(new Date())
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error")
        } finally {
            setLoading(false)
        }
    }, [fetchFn])

    useEffect(() => {
        // Initial fetch
        refetch()

        // Set up interval for auto-refresh
        const interval = setInterval(refetch, REFRESH_INTERVAL)

        return () => clearInterval(interval)
    }, [refetch])

    return { data, loading, error, refetch, lastUpdated }
}
