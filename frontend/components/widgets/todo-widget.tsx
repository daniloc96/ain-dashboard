"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckSquare, Trash2, Plus, GripVertical, Pencil, Check, X } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Todo } from "@/types"

// DnD Kit imports
import {
    DndContext,
    closestCenter,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
    DragEndEvent,
} from "@dnd-kit/core"
import {
    arrayMove,
    SortableContext,
    sortableKeyboardCoordinates,
    useSortable,
    verticalListSortingStrategy,
} from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Sortable Todo Item Component
function SortableTodoItem({
    todo,
    onToggle,
    onDelete,
    onEdit,
}: {
    todo: Todo
    onToggle: (id: number, completed: boolean) => void
    onDelete: (id: number) => void
    onEdit: (id: number, title: string) => void
}) {
    const [isEditing, setIsEditing] = React.useState(false)
    const [isExpanded, setIsExpanded] = React.useState(false)
    const [editValue, setEditValue] = React.useState(todo.title)

    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id: todo.id })

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1,
    }

    const handleSaveEdit = () => {
        if (editValue.trim() && editValue !== todo.title) {
            onEdit(todo.id, editValue.trim())
        } else {
            setEditValue(todo.title)
        }
        setIsEditing(false)
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter") {
            handleSaveEdit()
        } else if (e.key === "Escape") {
            setEditValue(todo.title)
            setIsEditing(false)
        }
    }

    return (
        <div
            ref={setNodeRef}
            style={style}
            className="flex items-center justify-between group bg-background rounded-md py-1"
        >
            <div className="flex items-center gap-2 flex-1 min-w-0">
                <button
                    {...attributes}
                    {...listeners}
                    className="cursor-grab active:cursor-grabbing touch-none opacity-0 group-hover:opacity-50 hover:!opacity-100 transition-opacity"
                >
                    <GripVertical className="h-4 w-4 text-muted-foreground" />
                </button>
                <Checkbox
                    checked={todo.completed}
                    onCheckedChange={(checked) => onToggle(todo.id, checked as boolean)}
                />
                {isEditing ? (
                    <textarea
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                        onBlur={handleSaveEdit}
                        onKeyDown={handleKeyDown}
                        className="text-sm flex-1 min-h-[28px] py-1 px-2 rounded-md border border-input bg-background resize-none overflow-hidden"
                        autoFocus
                        rows={1}
                        style={{ height: 'auto' }}
                        onInput={(e) => {
                            const target = e.target as HTMLTextAreaElement
                            target.style.height = 'auto'
                            target.style.height = target.scrollHeight + 'px'
                        }}
                    />
                ) : (
                    <span
                        className={`text-sm flex-1 cursor-pointer ${isExpanded ? '' : 'truncate'} ${todo.completed ? "line-through text-muted-foreground" : ""}`}
                        onClick={() => setIsExpanded(!isExpanded)}
                        onDoubleClick={() => setIsEditing(true)}
                    >
                        {todo.title}
                    </span>
                )}
            </div>
            <div className="flex items-center gap-1">
                {isEditing ? (
                    <>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6"
                            onClick={handleSaveEdit}
                        >
                            <Check className="h-3 w-3 text-green-500" />
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6"
                            onClick={() => {
                                setEditValue(todo.title)
                                setIsEditing(false)
                            }}
                        >
                            <X className="h-3 w-3 text-destructive" />
                        </Button>
                    </>
                ) : (
                    <>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => setIsEditing(true)}
                        >
                            <Pencil className="h-3 w-3 text-muted-foreground" />
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => onDelete(todo.id)}
                        >
                            <Trash2 className="h-3 w-3 text-destructive" />
                        </Button>
                    </>
                )}
            </div>
        </div>
    )
}

export function TodoWidget() {
    const [todos, setTodos] = React.useState<Todo[]>([])
    const [newTodo, setNewTodo] = React.useState("")
    const [loading, setLoading] = React.useState(true)

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8,
            },
        }),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    )

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
        setTodos(todos.map((t) => (t.id === id ? { ...t, completed } : t)))

        const todo = todos.find((t) => t.id === id)
        if (!todo) return

        try {
            await fetch(`${API_URL}/api/v1/todos/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: todo.title, completed }),
            })
        } catch (error) {
            console.error("Failed to update todo", error)
            fetchTodos()
        }
    }

    const editTodo = async (id: number, title: string) => {
        // Optimistic update
        setTodos(todos.map((t) => (t.id === id ? { ...t, title } : t)))

        const todo = todos.find((t) => t.id === id)
        if (!todo) return

        try {
            await fetch(`${API_URL}/api/v1/todos/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, completed: todo.completed }),
            })
        } catch (error) {
            console.error("Failed to edit todo", error)
            fetchTodos()
        }
    }

    const deleteTodo = async (id: number) => {
        setTodos(todos.filter((t) => t.id !== id))
        try {
            await fetch(`${API_URL}/api/v1/todos/${id}`, { method: "DELETE" })
        } catch (error) {
            console.error("Failed to delete todo", error)
            fetchTodos()
        }
    }

    const handleDragEnd = async (event: DragEndEvent) => {
        const { active, over } = event

        if (over && active.id !== over.id) {
            const oldIndex = todos.findIndex((t) => t.id === active.id)
            const newIndex = todos.findIndex((t) => t.id === over.id)
            const newTodos = arrayMove(todos, oldIndex, newIndex)

            // Optimistic update
            setTodos(newTodos)

            // Persist order to backend
            try {
                await fetch(`${API_URL}/api/v1/todos/reorder`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ order: newTodos.map((t) => t.id) }),
                })
            } catch (error) {
                console.error("Failed to reorder todos", error)
                fetchTodos()
            }
        }
    }

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Todo List</CardTitle>
                <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent className="flex-1 flex flex-col gap-4">
                <form onSubmit={addTodo} className="flex gap-2 items-end">
                    <textarea
                        value={newTodo}
                        onChange={(e) => setNewTodo(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault()
                                addTodo(e)
                            }
                        }}
                        placeholder="Add task..."
                        className="flex-1 min-h-[32px] max-h-[120px] py-1.5 px-3 text-sm rounded-md border border-input bg-background resize-none overflow-hidden"
                        rows={1}
                        onInput={(e) => {
                            const target = e.target as HTMLTextAreaElement
                            target.style.height = 'auto'
                            target.style.height = Math.min(target.scrollHeight, 120) + 'px'
                        }}
                    />
                    <Button type="submit" size="icon" className="h-8 w-8 shrink-0">
                        <Plus className="h-4 w-4" />
                    </Button>
                </form>

                <ScrollArea className="h-[200px] flex-1 pr-4">
                    {todos.length === 0 && !loading && (
                        <div className="text-muted-foreground text-sm text-center py-4">
                            No tasks pending.
                        </div>
                    )}
                    <DndContext
                        sensors={sensors}
                        collisionDetection={closestCenter}
                        onDragEnd={handleDragEnd}
                    >
                        <SortableContext
                            items={todos.map((t) => t.id)}
                            strategy={verticalListSortingStrategy}
                        >
                            <div className="space-y-1">
                                {todos.map((todo) => (
                                    <SortableTodoItem
                                        key={todo.id}
                                        todo={todo}
                                        onToggle={toggleTodo}
                                        onDelete={deleteTodo}
                                        onEdit={editTodo}
                                    />
                                ))}
                            </div>
                        </SortableContext>
                    </DndContext>
                </ScrollArea>
            </CardContent>
        </Card>
    )
}
