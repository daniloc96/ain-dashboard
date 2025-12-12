"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckSquare, Trash2, Plus } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Todo } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export function TodoWidget() {
    const [todos, setTodos] = React.useState<Todo[]>([])
    const [newTodo, setNewTodo] = React.useState("")
    const [loading, setLoading] = React.useState(true)

    const fetchTodos = async () => {
        try {
            const res = await fetch(`${API_URL}/api/v1/todos/`)
            if (res.ok) {
                const data = await res.json()
                setTodos(data)
            }
        } catch (error) {
            console.error("Failed to fetch todos", error)
        } finally {
            setLoading(false)
        }
    }

    React.useEffect(() => {
        fetchTodos()
    }, [])

    const addTodo = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!newTodo.trim()) return

        try {
            const res = await fetch(`${API_URL}/api/v1/todos/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: newTodo }),
            })
            if (res.ok) {
                const item = await res.json()
                setTodos([...todos, item])
                setNewTodo("")
            }
        } catch (error) {
            console.error("Failed to add todo", error)
        }
    }

    const toggleTodo = async (id: number, completed: boolean) => {
        // Optimistic update
        setTodos(todos.map(t => t.id === id ? { ...t, completed } : t))

        // Find title
        const todo = todos.find(t => t.id === id)
        if (!todo) return

        try {
            await fetch(`${API_URL}/api/v1/todos/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: todo.title, completed }),
            })
        } catch (error) {
            console.error("Failed to update todo", error)
            fetchTodos() // Revert on error
        }
    }

    const deleteTodo = async (id: number) => {
        setTodos(todos.filter(t => t.id !== id))
        try {
            await fetch(`${API_URL}/api/v1/todos/${id}`, { method: "DELETE" })
        } catch (error) {
            console.error("Failed to delete todo", error)
            fetchTodos()
        }
    }

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Todo List</CardTitle>
                <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent className="flex-1 flex flex-col gap-4">
                <form onSubmit={addTodo} className="flex gap-2">
                    <Input
                        value={newTodo}
                        onChange={(e) => setNewTodo(e.target.value)}
                        placeholder="Add task..."
                        className="h-8"
                    />
                    <Button type="submit" size="icon" className="h-8 w-8">
                        <Plus className="h-4 w-4" />
                    </Button>
                </form>

                <ScrollArea className="h-[200px] flex-1 pr-4">
                    {todos.length === 0 && !loading && (
                        <div className="text-muted-foreground text-sm text-center py-4">No tasks pending.</div>
                    )}
                    <div className="space-y-2">
                        {todos.map((todo) => (
                            <div key={todo.id} className="flex items-center justify-between group">
                                <div className="flex items-center gap-2">
                                    <Checkbox
                                        checked={todo.completed}
                                        onCheckedChange={(checked) => toggleTodo(todo.id, checked as boolean)}
                                    />
                                    <span className={`text-sm ${todo.completed ? 'line-through text-muted-foreground' : ''}`}>
                                        {todo.title}
                                    </span>
                                </div>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                                    onClick={() => deleteTodo(todo.id)}
                                >
                                    <Trash2 className="h-3 w-3 text-destructive" />
                                </Button>
                            </div>
                        ))}
                    </div>
                </ScrollArea>
            </CardContent>
        </Card>
    )
}
