#!/usr/bin/env python3
"""
MCP Tool Handlers
=================
This module contains the handler functions for each MCP tool.
Each handler processes tool arguments, calls the appropriate Google API client method,
and formats the response for the MCP client.

The handlers are organized by functionality (calendar vs photos) and include
comprehensive error handling and response formatting.
"""

import logging
from typing import List
import mcp.types as types
from google_api_client import GoogleAPIClient

# Configure logging for this module
logger = logging.getLogger(__name__)

class ToolHandlers:
    """
    Container class for all MCP tool handler methods
    
    This class encapsulates all the tool handling logic and maintains a reference
    to the Google API client for making API calls.
    """
    
    def __init__(self, google_client: GoogleAPIClient):
        """
        Initialize the tool handlers
        
        Args:
            google_client: Instance of GoogleAPIClient for making API calls
        """
        self.google_client = google_client
    
    # =============================================================================
    # CALENDAR TOOL HANDLERS
    # =============================================================================
    
    async def handle_create_calendar_event(self, arguments: dict) -> List[types.TextContent]:
        """
        Handle the create_calendar_event tool call
        
        Args:
            arguments: Dictionary containing tool arguments
                - summary (str): Event title
                - start_time (str): Start time in ISO format
                - end_time (str): End time in ISO format
                - description (str, optional): Event description
                - location (str, optional): Event location
                - calendar_id (str, optional): Target calendar ID
                
        Returns:
            List[types.TextContent]: Formatted response with event creation details
        """
        logger.info(f"Creating calendar event: {arguments.get('summary', 'Untitled')}")
        
        try:
            # Call the Google API client method
            event_id = await self.google_client.create_calendar_event(
                summary=arguments["summary"],
                start_time=arguments["start_time"],
                end_time=arguments["end_time"],
                description=arguments.get("description", ""),
                location=arguments.get("location", ""),
                calendar_id=arguments.get("calendar_id", "primary")
            )
            
            # Return success message with event ID and details
            return [types.TextContent(
                type="text",
                text=f"✅ Calendar event created successfully!\n"
                     f"Event ID: {event_id}\n"
                     f"Title: {arguments['summary']}\n"
                     f"Start: {arguments['start_time']}\n"
                     f"End: {arguments['end_time']}"
            )]
            
        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            return [types.TextContent(
                type="text",
                text=f"❌ Error creating calendar event: {str(e)}"
            )]
    
    async def handle_get_calendar_events(self, arguments: dict) -> List[types.TextContent]:
        """
        Handle the get_calendar_events tool call
        
        Args:
            arguments: Dictionary containing tool arguments
                - calendar_id (str, optional): Calendar ID to query
                - max_results (int, optional): Maximum number of events to return
                
        Returns:
            List[types.TextContent]: Formatted list of upcoming events
        """
        logger.info("Retrieving calendar events")
        
        try:
            # Call the Google API client method
            events = await self.google_client.get_calendar_events(
                calendar_id=arguments.get("calendar_id", "primary"),
                max_results=arguments.get("max_results", 10)
            )
            
            # Handle case where no events are found
            if not events:
                return [types.TextContent(
                    type="text",
                    text="📅 No upcoming events found in your calendar."
                )]
            
            # Format the response with event details
            events_text = f"📅 Found {len(events)} upcoming calendar events:\n\n"
            
            for i, event in enumerate(events, 1):
                # Extract start time (could be dateTime or date for all-day events)
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                events_text += f"{i}. **{event['summary']}**\n"
                events_text += f"   🕒 Time: {start}\n"
                events_text += f"   🆔 ID: {event['id']}\n"
                
                # Add optional fields if they exist
                if event.get('location'):
                    events_text += f"   📍 Location: {event['location']}\n"
                if event.get('description'):
                    # Truncate long descriptions
                    desc = event['description'][:100] + "..." if len(event['description']) > 100 else event['description']
                    events_text += f"   📝 Description: {desc}\n"
                events_text += "\n"
            
            return [types.TextContent(type="text", text=events_text)]
            
        except Exception as e:
            logger.error(f"Error retrieving calendar events: {e}")
            return [types.TextContent(
                type="text",
                text=f"❌ Error retrieving calendar events: {str(e)}"
            )]
    
    async def handle_update_calendar_event(self, arguments: dict) -> List[types.TextContent]:
        """
        Handle the update_calendar_event tool call
        
        Args:
            arguments: Dictionary containing tool arguments
                - event_id (str): ID of event to update
                - summary (str, optional): New event title
                - start_time (str, optional): New start time
                - end_time (str, optional): New end time
                - description (str, optional): New description
                - location (str, optional): New location
                - calendar_id (str, optional): Calendar ID
                
        Returns:
            List[types.TextContent]: Formatted response with update confirmation
        """
        logger.info(f"Updating calendar event: {arguments['event_id']}")
        
        try:
            # Call the Google API client method
            success = await self.google_client.update_calendar_event(
                event_id=arguments["event_id"],
                summary=arguments.get("summary"),
                start_time=arguments.get("start_time"),
                end_time=arguments.get("end_time"),
                description=arguments.get("description"),
                location=arguments.get("location"),
                calendar_id=arguments.get("calendar_id", "primary")
            )
            
            # Build update summary for user feedback
            updates = []
            if arguments.get("summary"):
                updates.append(f"Title: {arguments['summary']}")
            if arguments.get("start_time"):
                updates.append(f"Start: {arguments['start_time']}")
            if arguments.get("end_time"):
                updates.append(f"End: {arguments['end_time']}")
            if "description" in arguments:
                updates.append("Description updated")
            if "location" in arguments:
                updates.append(f"Location: {arguments.get('location', 'Cleared')}")
            
            update_text = "\n".join(f"  • {update}" for update in updates)
            
            return [types.TextContent(
                type="text",
                text=f"✅ Calendar event updated successfully!\n"
                     f"Event ID: {arguments['event_id']}\n"
                     f"Updates made:\n{update_text}"
            )]
            
        except Exception as e:
            logger.error(f"Error updating calendar event: {e}")
            return [types.TextContent(
                type="text",
                text=f"❌ Error updating calendar event: {str(e)}"
            )]
    
    async def handle_delete_calendar_event(self, arguments: dict) -> List[types.TextContent]:
        """
        Handle the delete_calendar_event tool call
        
        Args:
            arguments: Dictionary containing tool arguments
                - event_id (str): ID of event to delete
                - calendar_id (str, optional): Calendar ID
                
        Returns:
            List[types.TextContent]: Formatted response with deletion confirmation
        """
        logger.info(f"Deleting calendar event: {arguments['event_id']}")
        
        try:
            # Call the Google API client method
            success = await self.google_client.delete_calendar_event(
                event_id=arguments["event_id"],
                calendar_id=arguments.get("calendar_id", "primary")
            )
            
            return [types.TextContent(
                type="text",
                text=f"✅ Calendar event deleted successfully!\n"
                     f"Event ID: {arguments['event_id']}"
            )]
            
        except Exception as e:
            logger.error(f"Error deleting calendar event: {e}")
            return [types.TextContent(
                type="text",
                text=f"❌ Error deleting calendar event: {str(e)}"
            )]

    # =============================================================================
    # PHOTOS TOOL HANDLERS
    # =============================================================================
    
    async def handle_get_photos(self, arguments: dict) -> List[types.TextContent]:
        """
        Handle the get_photos tool call
        
        Args:
            arguments: Dictionary containing tool arguments
                - page_size (int, optional): Number of photos to retrieve
                
        Returns:
            List[types.TextContent]: Formatted list of photos with metadata
        """
        logger.info("Retrieving photos from Google Photos")
        
        try:
            # Call the Google API client method
            photos = await self.google_client.get_photos(
                page_size=arguments.get("page_size", 25)
            )
            
            # Handle case where no photos are found
            if not photos:
                return [types.TextContent(
                    type="text",
                    text="📸 No photos found in your Google Photos library."
                )]
            
            # Format the response with photo details
            photos_text = f"📸 Found {len(photos)} photos in your Google Photos library:\n\n"
            
            for i, photo in enumerate(photos, 1):
                photos_text += f"{i}. **{photo['filename']}**\n"
                photos_text += f"   🆔 ID: {photo['id']}\n"
                photos_text += f"   📄 Type: {photo['mimeType']}\n"
                
                # Add creation time if available
                if 'mediaMetadata' in photo:
                    creation_time = photo['mediaMetadata'].get('creationTime', 'Unknown')
                    # Format the timestamp for better readability
                    if creation_time != 'Unknown':
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                            photos_text += f"   📅 Created: {formatted_time}\n"
                        except:
                            photos_text += f"   📅 Created: {creation_time}\n"
                
                # Add photo dimensions if available
                if 'mediaMetadata' in photo and 'photo' in photo['mediaMetadata']:
                    photo_meta = photo['mediaMetadata']['photo']
                    if 'cameraMake' in photo_meta:
                        photos_text += f"   📷 Camera: {photo_meta['cameraMake']}"
                        if 'cameraModel' in photo_meta:
                            photos_text += f" {photo_meta['cameraModel']}"
                        photos_text += "\n"
                
                photos_text += "\n"
            
            return [types.TextContent(type="text", text=photos_text)]
            
        except Exception as e:
            logger.error(f"Error retrieving photos: {e}")
            return [types.TextContent(
                type="text",
                text=f"❌ Error retrieving photos: {str(e)}"
            )]
    
    async def handle_search_photos(self, arguments: dict) -> List[types.TextContent]:
        """
        Handle the search_photos tool call
        
        Args:
            arguments: Dictionary containing tool arguments
                - start_date (str, optional): Start date for search
                - end_date (str, optional): End date for search
                - media_type (str, optional): Media type filter
                - page_size (int, optional): Number of results to return
                
        Returns:
            List[types.TextContent]: Formatted list of photos matching search criteria
        """
        logger.info("Searching photos in Google Photos")
        
        try:
            # Call the Google API client method
            photos = await self.google_client.search_photos(
                start_date=arguments.get("start_date"),
                end_date=arguments.get("end_date"),
                media_type=arguments.get("media_type"),
                page_size=arguments.get("page_size", 25)
            )
            
            # Build search criteria description for user feedback
            criteria = []
            if arguments.get("start_date"):
                criteria.append(f"after {arguments['start_date']}")
            if arguments.get("end_date"):
                criteria.append(f"before {arguments['end_date']}")
            if arguments.get("media_type"):
                criteria.append(f"type: {arguments['media_type']}")
            
            criteria_text = " and ".join(criteria) if criteria else "no filters"
            
            # Handle case where no photos are found
            if not photos:
                return [types.TextContent(
                    type="text",
                    text=f"📸 No photos found matching search criteria ({criteria_text})."
                )]
            
            # Format the response with photo details
            photos_text = f"📸 Found {len(photos)} photos matching search criteria ({criteria_text}):\n\n"
            
            for i, photo in enumerate(photos, 1):
                photos_text += f"{i}. **{photo['filename']}**\n"
                photos_text += f"   🆔 ID: {photo['id']}\n"
                photos_text += f"   📄 Type: {photo['mimeType']}\n"
                
                # Add creation time if available
                if 'mediaMetadata' in photo:
                    creation_time = photo['mediaMetadata'].get('creationTime', 'Unknown')
                    if creation_time != 'Unknown':
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                            photos_text += f"   📅 Created: {formatted_time}\n"
                        except:
                            photos_text += f"   📅 Created: {creation_time}\n"
                
                photos_text += "\n"
            
            return [types.TextContent(type="text", text=photos_text)]
            
        except Exception as e:
            logger.error(f"Error searching photos: {e}")
            return [types.TextContent(
                type="text",
                text=f"❌ Error searching photos: {str(e)}"
            )]
    
    async def handle_get_photo_download_url(self, arguments: dict) -> List[types.TextContent]:
        """
        Handle the get_photo_download_url tool call
        
        Args:
            arguments: Dictionary containing tool arguments
                - photo_id (str): ID of photo to get download URL for
                
        Returns:
            List[types.TextContent]: Formatted response with download URL
        """
        logger.info(f"Getting download URL for photo: {arguments['photo_id']}")
        
        try:
            # Call the Google API client method
            download_url = await self.google_client.get_photo_download_url(
                photo_id=arguments["photo_id"]
            )
            
            return [types.TextContent(
                type="text",
                text=f"📸 Download URL for photo {arguments['photo_id']}:\n\n"
                     f"🔗 **URL:** {download_url}\n\n"
                     f"⚠️ **Note:** This URL expires in approximately 1 hour for security reasons.\n"
                     f"Use it promptly to download the full-resolution photo."
            )]
            
        except Exception as e:
            logger.error(f"Error getting photo download URL: {e}")
            return [types.TextContent(
                type="text",
                text=f"❌ Error getting photo download URL: {str(e)}"
            )]

    # =============================================================================
    # TOOL ROUTING
    # =============================================================================
    
    async def handle_tool_call(self, name: str, arguments: dict) -> List[types.TextContent]:
        """
        Route tool calls to the appropriate handler method
        
        This method acts as a dispatcher, calling the correct handler based on the tool name.
        It also ensures authentication is handled before any API calls are made.
        
        Args:
            name: Name of the tool being called
            arguments: Dictionary of arguments passed to the tool
            
        Returns:
            List[types.TextContent]: Formatted response from the appropriate handler
        """
        try:
            # Ensure we have valid credentials before making any API calls
            if not self.google_client.creds:
                logger.info("No credentials found, initiating authentication")
                await self.google_client.authenticate()
                await self.google_client.build_services()
            
            # Route to appropriate handler based on tool name
            if name == "create_calendar_event":
                return await self.handle_create_calendar_event(arguments)
            elif name == "get_calendar_events":
                return await self.handle_get_calendar_events(arguments)
            elif name == "update_calendar_event":
                return await self.handle_update_calendar_event(arguments)
            elif name == "delete_calendar_event":
                return await self.handle_delete_calendar_event(arguments)
            elif name == "get_photos":
                return await self.handle_get_photos(arguments)
            elif name == "search_photos":
                return await self.handle_search_photos(arguments)
            elif name == "get_photo_download_url":
                return await self.handle_get_photo_download_url(arguments)
            else:
                # Handle unknown tool names
                logger.warning(f"Unknown tool requested: {name}")
                return [types.TextContent(
                    type="text",
                    text=f"❌ Unknown tool: {name}\n"
                         f"Available tools: create_calendar_event, get_calendar_events, "
                         f"update_calendar_event, delete_calendar_event, get_photos, "
                         f"search_photos, get_photo_download_url"
                )]
        
        except Exception as e:
            # Catch-all error handler for any unexpected errors
            logger.error(f"Unexpected error executing tool {name}: {e}")
            return [types.TextContent(
                type="text",
                text=f"❌ Unexpected error executing tool {name}: {str(e)}"
            )]