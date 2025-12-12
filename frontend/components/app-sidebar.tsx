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
                    <SidebarGroupLabel>AIN Dashboard</SidebarGroupLabel>
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
