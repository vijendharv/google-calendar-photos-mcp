#!/usr/bin/env python3
"""
MCP Tools Definitions
=====================
This module defines all the MCP tools that the server exposes to clients.
It separates tool definitions from the server logic for better maintainability.

Each tool definition includes:
- name: Unique identifier for the tool
- description: Human-readable description of what the tool does
- inputSchema: JSON Schema defining the expected input parameters
"""

import mcp.types as types
from typing import List

def get_calendar_tools() -> List[types.Tool]:
    """
    Define calendar-related MCP tools
    
    Returns:
        List[types.Tool]: List of calendar tool definitions
    """
    return [
        types.Tool(
            name="create_calendar_event",
            description="Create a new Google Calendar event with specified details",
            inputSchema={
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string", 
                        "description": "Event title or name (required)"
                    },
                    "start_time": {
                        "type": "string", 
                        "description": "Event start time in ISO 8601 format (e.g., '2024-01-15T14:00:00Z')"
                    },
                    "end_time": {
                        "type": "string", 
                        "description": "Event end time in ISO 8601 format (e.g., '2024-01-15T15:00:00Z')"
                    },
                    "description": {
                        "type": "string", 
                        "description": "Detailed event description (optional)",
                        "default": ""
                    },
                    "location": {
                        "type": "string", 
                        "description": "Event location or address (optional)",
                        "default": ""
                    },
                    "calendar_id": {
                        "type": "string", 
                        "description": "Target calendar ID ('primary' for main calendar)",
                        "default": "primary"
                    }
                },
                "required": ["summary", "start_time", "end_time"]  # These fields are mandatory
            }
        ),
        
        types.Tool(
            name="get_calendar_events",
            description="Retrieve upcoming events from Google Calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string", 
                        "description": "Calendar ID to query ('primary' for main calendar)",
                        "default": "primary"
                    },
                    "max_results": {
                        "type": "integer", 
                        "description": "Maximum number of events to return (1-2500)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 2500
                    }
                }
                # No required fields - all parameters have defaults
            }
        ),
        
        types.Tool(
            name="update_calendar_event",
            description="Update an existing Google Calendar event. Only specified fields will be changed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string", 
                        "description": "Unique ID of the event to update (required)"
                    },
                    "summary": {
                        "type": "string", 
                        "description": "New event title (optional)"
                    },
                    "start_time": {
                        "type": "string", 
                        "description": "New start time in ISO 8601 format (optional)"
                    },
                    "end_time": {
                        "type": "string", 
                        "description": "New end time in ISO 8601 format (optional)"
                    },
                    "description": {
                        "type": "string", 
                        "description": "New event description (optional)"
                    },
                    "location": {
                        "type": "string", 
                        "description": "New event location (optional)"
                    },
                    "calendar_id": {
                        "type": "string", 
                        "description": "Calendar ID containing the event",
                        "default": "primary"
                    }
                },
                "required": ["event_id"]  # Only event_id is required
            }
        ),
        
        types.Tool(
            name="delete_calendar_event",
            description="Delete a Google Calendar event permanently",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string", 
                        "description": "Unique ID of the event to delete (required)"
                    },
                    "calendar_id": {
                        "type": "string", 
                        "description": "Calendar ID containing the event",
                        "default": "primary"
                    }
                },
                "required": ["event_id"]
            }
        )
    ]

def get_photos_tools() -> List[types.Tool]:
    """
    Define photos-related MCP tools
    
    Returns:
        List[types.Tool]: List of photos tool definitions
    """
    return [
        types.Tool(
            name="get_photos",
            description="Retrieve recent photos from Google Photos library",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_size": {
                        "type": "integer", 
                        "description": "Number of photos to retrieve (1-100)",
                        "default": 25,
                        "minimum": 1,
                        "maximum": 100
                    }
                }
                # No required fields
            }
        ),
        
        types.Tool(
            name="search_photos",
            description="Search photos in Google Photos with date and type filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string", 
                        "description": "Start date for search in ISO 8601 format (e.g., '2024-01-01T00:00:00Z')"
                    },
                    "end_date": {
                        "type": "string", 
                        "description": "End date for search in ISO 8601 format (e.g., '2024-01-31T23:59:59Z')"
                    },
                    "media_type": {
                        "type": "string", 
                        "description": "Filter by media type: 'PHOTO' for images only, 'VIDEO' for videos only",
                        "enum": ["PHOTO", "VIDEO"]
                    },
                    "page_size": {
                        "type": "integer", 
                        "description": "Number of results to return (1-100)",
                        "default": 25,
                        "minimum": 1,
                        "maximum": 100
                    }
                }
                # No required fields - all filters are optional
            }
        ),
        
        types.Tool(
            name="get_photo_download_url",
            description="Get a download URL for a specific photo from Google Photos",
            inputSchema={
                "type": "object",
                "properties": {
                    "photo_id": {
                        "type": "string", 
                        "description": "Unique ID of the photo (obtained from get_photos or search_photos)"
                    }
                },
                "required": ["photo_id"]
            }
        )
    ]

def get_all_tools() -> List[types.Tool]:
    """
    Get all available MCP tools (calendar + photos)
    
    Returns:
        List[types.Tool]: Complete list of all tool definitions
    """
    return get_calendar_tools() + get_photos_tools()