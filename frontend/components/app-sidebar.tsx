"use client"

import { Calendar, Home, Inbox, Search, Settings, ListTodo, GitPullRequest, Hash } from "lucide-react"

import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarRail,
} from "@/components/ui/sidebar"

// Menu items.
const items = [
    {
        title: "Home",
        url: "/",
        icon: Home,
    },
    {
        title: "Todo",
        url: "/todo",
        icon: ListTodo,
    },
    {
        title: "Pull Requests",
        url: "/prs",
        icon: GitPullRequest,
    },
    {
        title: "Jira",
        url: "/jira",
        icon: Hash,
    },
    {
        title: "Calendar",
        url: "/calendar",
        icon: Calendar,
    },
]

export function AppSidebar() {
    return (
        <Sidebar collapsible="icon" className="border-r border-sidebar-border bg-sidebar">
            <SidebarContent>
                <SidebarGroup>
                    <div className="flex items-center gap-3 px-2 py-2 mb-2">
                        <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground overflow-hidden">
                            <img src="/logo-glyph.png" alt="AIN" className="size-full object-cover" />
                        </div>
                        <div className="flex flex-col gap-0.5 leading-none">
                            <span className="font-semibold">AIN Dashboard</span>
                            <span className="text-xs text-muted-foreground">v1.0.0</span>
                        </div>
                    </div>
                    <SidebarGroupLabel>Navigation</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {items.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton asChild tooltip={item.title}>
                                        <a href={item.url}>
                                            <item.icon />
                                            <span>{item.title}</span>
                                        </a>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
            <SidebarRail />
        </Sidebar>
    )
}
