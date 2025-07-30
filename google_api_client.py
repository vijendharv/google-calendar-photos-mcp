#!/usr/bin/env python3
"""
Google API Client Module
========================
This module provides a client class for Google Calendar and Photos APIs.
It handles OAuth2 authentication, token management, and API operations.

The GoogleAPIClient class encapsulates all Google API interactions and can be
used independently of the MCP server for other applications.
"""

import os
import pickle
import logging
from datetime import datetime
from typing import List, Dict, Optional

# Google API imports for authentication and service building
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging for this module
logger = logging.getLogger(__name__)

class GoogleAPIClient:
    """
    Client class for Google Calendar and Photos APIs
    
    This class handles:
    1. OAuth2 authentication flow
    2. Token storage and refresh
    3. Service object creation for Calendar and Photos APIs
    4. Individual API operations (CRUD for calendar, read operations for photos)
    
    The class uses the Google API Python Client library and follows OAuth2 best practices
    by storing tokens locally and refreshing them automatically when needed.
    """
    
    # Define the required OAuth2 scopes for both Calendar and Photos APIs
    # These scopes determine what permissions the application will request from users
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',                    # Full calendar access
        'https://www.googleapis.com/auth/photoslibrary',              # Photos library access
        'https://www.googleapis.com/auth/photoslibrary.readonly'      # Read-only photos access
    ]
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.pickle'):
        """
        Initialize the Google API client
        
        Args:
            credentials_file: Path to the OAuth2 client credentials JSON file 
                             (downloaded from Google Cloud Console)
            token_file: Path where access/refresh tokens will be stored
                       (created automatically after first authentication)
        """
        self.credentials_file = credentials_file  # OAuth2 client credentials
        self.token_file = token_file             # Stored user tokens
        self.creds = None                        # Will hold current credentials
        self.calendar_service = None             # Calendar API service object
        self.photos_service = None               # Photos API service object
        
    async def authenticate(self):
        """
        Handle OAuth2 authentication flow
        
        This method:
        1. Tries to load existing tokens from disk
        2. Checks if tokens are valid and refreshes if needed
        3. If no valid tokens exist, runs the OAuth2 flow to get new ones
        4. Saves tokens to disk for future use
        
        The OAuth2 flow will open a browser window for user consent on first run.
        Subsequent runs will use stored tokens automatically.
        """
        # Step 1: Try to load existing tokens from pickle file
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
                logger.info("Loaded existing credentials from token file")
        
        # Step 2: Check if credentials are valid or need refresh
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # We have expired credentials but a valid refresh token
                logger.info("Refreshing expired credentials")
                self.creds.refresh(Request())
            else:
                # No valid credentials - need to run OAuth2 flow
                logger.info("No valid credentials found, starting OAuth2 flow")
                
                # Check if credentials file exists
                if not os.path.exists(self.credentials_file):
                    logger.error(f"Credentials file not found: {self.credentials_file}")
                    logger.error(f"Current working directory: {os.getcwd()}")
                    logger.error(f"Credentials file absolute path: {os.path.abspath(self.credentials_file)}")
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        f"Absolute path: {os.path.abspath(self.credentials_file)}\n"
                        f"Current working directory: {os.getcwd()}\n"
                        f"Please download OAuth2 credentials from Google Cloud Console"
                    )
                
                # Run OAuth2 flow - this will open a browser window
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
                logger.info("OAuth2 flow completed successfully")
            
            # Step 3: Save credentials for future use
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
                logger.info("Saved credentials to token file")
    
    async def build_services(self):
        """
        Build Google API service objects for Calendar and Photos
        
        Service objects are the main interface for making API calls.
        They handle request formatting, authentication headers, and response parsing.
        
        Raises:
            HttpError: If there's an error building the services (e.g., invalid credentials)
        """
        try:
            # Build Calendar API service (v3 is the current stable version)
            self.calendar_service = build('calendar', 'v3', credentials=self.creds)
            
            # Build Photos API service (v1 is the current stable version)
            # self.photos_service = build('photoslibrary', 'v1', credentials=self.creds)
            
            logger.info("Successfully built Google API service objects")
        except HttpError as error:
            logger.error(f"Error building API services: {error}")
            raise

    # =============================================================================
    # CALENDAR API OPERATIONS
    # =============================================================================

    async def create_calendar_event(self, summary: str, start_time: str, end_time: str, 
                                  description: str = "", location: str = "", calendar_id: str = 'primary') -> str:
        """
        Create a new calendar event
        
        Args:
            summary: Event title/name (required)
            start_time: Event start time in ISO format (e.g., "2024-01-15T14:00:00Z")
            end_time: Event end time in ISO format (e.g., "2024-01-15T15:00:00Z")
            description: Optional event description
            location: Optional event location
            calendar_id: ID of calendar to create event in ('primary' = user's main calendar)
            
        Returns:
            str: The unique ID of the created event
            
        Raises:
            HttpError: If the API call fails (e.g., invalid parameters, auth issues)
        """
        # Build the event object according to Google Calendar API schema
        event = {
            'summary': summary,           # Event title
            'location': location,         # Event location (optional)
            'description': description,   # Event description (optional)
            'start': {
                'dateTime': start_time,   # Start time in ISO format
                'timeZone': 'UTC',        # Timezone (could be made configurable)
            },
            'end': {
                'dateTime': end_time,     # End time in ISO format
                'timeZone': 'UTC',        # Timezone (could be made configurable)
            },
        }
        
        try:
            # Make the API call to create the event
            created_event = self.calendar_service.events().insert(
                calendarId=calendar_id, body=event).execute()
            
            logger.info(f"Created calendar event: {summary} (ID: {created_event['id']})")
            return created_event['id']
            
        except HttpError as error:
            logger.error(f"Error creating calendar event: {error}")
            raise
    
    async def get_calendar_events(self, calendar_id: str = 'primary', max_results: int = 10) -> List[Dict]:
        """
        Retrieve upcoming calendar events
        
        Args:
            calendar_id: ID of calendar to query ('primary' = user's main calendar)
            max_results: Maximum number of events to return (1-2500)
            
        Returns:
            List[Dict]: List of event objects containing event details
            
        Each event dict contains fields like:
            - id: Unique event identifier
            - summary: Event title
            - start/end: Time information
            - description: Event description (if any)
            - location: Event location (if any)
            
        Raises:
            HttpError: If the API call fails
        """
        try:
            # Get current time in RFC3339 format for filtering future events
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            
            # Make API call to list events
            events_result = self.calendar_service.events().list(
                calendarId=calendar_id,    # Which calendar to query
                timeMin=now,               # Only get events after current time
                maxResults=max_results,    # Limit number of results
                singleEvents=True,         # Expand recurring events into individual instances
                orderBy='startTime'        # Sort by start time (required when singleEvents=True)
            ).execute()
            
            # Extract the events list from the response
            events = events_result.get('items', [])
            
            logger.info(f"Retrieved {len(events)} upcoming events from calendar {calendar_id}")
            return events
            
        except HttpError as error:
            logger.error(f"Error retrieving calendar events: {error}")
            raise
    
    async def update_calendar_event(self, event_id: str, summary: str = None, 
                                  start_time: str = None, end_time: str = None,
                                  description: str = None, location: str = None,
                                  calendar_id: str = 'primary') -> bool:
        """
        Update an existing calendar event
        
        This method follows the "patch" pattern: only provided fields are updated,
        existing fields that aren't specified remain unchanged.
        
        Args:
            event_id: Unique ID of the event to update (required)
            summary: New event title (optional)
            start_time: New start time in ISO format (optional)
            end_time: New end time in ISO format (optional)
            description: New event description (optional, None clears existing)
            location: New event location (optional, None clears existing)
            calendar_id: ID of calendar containing the event
            
        Returns:
            bool: True if update was successful
            
        Raises:
            HttpError: If the API call fails (e.g., event not found, no permission)
        """
        try:
            # Step 1: Get the current event data
            event = self.calendar_service.events().get(
                calendarId=calendar_id, eventId=event_id).execute()
            
            logger.info(f"Retrieved existing event for update: {event.get('summary', 'Untitled')}")
            
            # Step 2: Update only the fields that were provided
            if summary:
                event['summary'] = summary
                logger.info(f"Updated summary to: {summary}")
                
            if description is not None:  # Check for None specifically to allow empty string
                event['description'] = description
                logger.info(f"Updated description")
                
            if location is not None:  # Check for None specifically to allow empty string
                event['location'] = location
                logger.info(f"Updated location to: {location}")
                
            if start_time:
                event['start'] = {'dateTime': start_time, 'timeZone': 'UTC'}
                logger.info(f"Updated start time to: {start_time}")
                
            if end_time:
                event['end'] = {'dateTime': end_time, 'timeZone': 'UTC'}
                logger.info(f"Updated end time to: {end_time}")
            
            # Step 3: Send the updated event back to the API
            updated_event = self.calendar_service.events().update(
                calendarId=calendar_id, eventId=event_id, body=event).execute()
            
            logger.info(f"Successfully updated event {event_id}")
            return True
            
        except HttpError as error:
            logger.error(f"Error updating calendar event {event_id}: {error}")
            raise
    
    async def delete_calendar_event(self, event_id: str, calendar_id: str = 'primary') -> bool:
        """
        Delete a calendar event
        
        Args:
            event_id: Unique ID of the event to delete (required)
            calendar_id: ID of calendar containing the event
            
        Returns:
            bool: True if deletion was successful
            
        Raises:
            HttpError: If the API call fails (e.g., event not found, no permission)
            
        Note: Deleted events cannot be recovered through the API
        """
        try:
            # Make API call to delete the event
            self.calendar_service.events().delete(
                calendarId=calendar_id, eventId=event_id).execute()
            
            logger.info(f"Successfully deleted calendar event {event_id}")
            return True
            
        except HttpError as error:
            logger.error(f"Error deleting calendar event {event_id}: {error}")
            raise

    # =============================================================================
    # GOOGLE PHOTOS API OPERATIONS  
    # =============================================================================

    async def get_photos(self, page_size: int = 25) -> List[Dict]:
        """
        Retrieve photos from Google Photos library
        
        This returns the most recent photos from the user's library.
        Photos are returned in reverse chronological order (newest first).
        
        Args:
            page_size: Number of photos to retrieve (1-100, default 25)
            
        Returns:
            List[Dict]: List of photo metadata objects
            
        Each photo dict contains fields like:
            - id: Unique photo identifier
            - filename: Original filename
            - mimeType: File type (e.g., 'image/jpeg')
            - mediaMetadata: Technical details (dimensions, creation time, etc.)
            - baseUrl: URL for accessing the photo (temporary, expires in ~1 hour)
            
        Raises:
            HttpError: If the API call fails
        """
        try:
            # Make API call to list media items (photos and videos)
            results = self.photos_service.mediaItems().list(
                pageSize=page_size  # Limit number of items returned
            ).execute()
            
            # Extract items from response (could be empty list)
            items = results.get('mediaItems', [])
            
            logger.info(f"Retrieved {len(items)} photos from Google Photos")
            return items
            
        except HttpError as error:
            logger.error(f"Error retrieving photos from Google Photos: {error}")
            raise
    
    async def search_photos(self, start_date: str = None, end_date: str = None,
                           media_type: str = None, page_size: int = 25) -> List[Dict]:
        """
        Search photos in Google Photos with various filters
        
        This method allows filtering photos by date range and media type.
        All filters are optional and can be combined.
        
        Args:
            start_date: Start date for search in ISO format (e.g., "2024-01-01T00:00:00Z")
            end_date: End date for search in ISO format (e.g., "2024-01-31T23:59:59Z")
            media_type: Filter by media type - 'PHOTO' or 'VIDEO'
            page_size: Number of results to return (1-100, default 25)
            
        Returns:
            List[Dict]: List of photo metadata objects matching the search criteria
            
        Raises:
            HttpError: If the API call fails
            ValueError: If date strings are not in valid format
        """
        try:
            # Build filters object based on provided parameters
            filters = {}
            
            # Add date range filter if either start or end date is provided
            if start_date or end_date:
                date_filter = {}
                
                if start_date:
                    # Parse ISO date string and convert to Google's date format
                    dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    date_filter['startDate'] = {
                        'year': dt.year,
                        'month': dt.month, 
                        'day': dt.day
                    }
                    logger.info(f"Added start date filter: {dt.date()}")
                
                if end_date:
                    # Parse ISO date string and convert to Google's date format
                    dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    date_filter['endDate'] = {
                        'year': dt.year,
                        'month': dt.month,
                        'day': dt.day
                    }
                    logger.info(f"Added end date filter: {dt.date()}")
                
                # Add the complete date range filter
                filters['dateFilter'] = {'ranges': [date_filter]}
            
            # Add media type filter if specified
            if media_type:
                filters['mediaTypeFilter'] = {'mediaTypes': [media_type]}
                logger.info(f"Added media type filter: {media_type}")
            
            # Build the search request
            search_request = {
                'pageSize': page_size,
                'filters': filters if filters else None  # Only include filters if we have any
            }
            
            # Make API call to search for photos
            results = self.photos_service.mediaItems().search(
                body=search_request).execute()
            
            # Extract items from response
            items = results.get('mediaItems', [])
            
            logger.info(f"Found {len(items)} photos matching search criteria")
            return items
            
        except HttpError as error:
            logger.error(f"Error searching photos in Google Photos: {error}")
            raise
        except ValueError as error:
            logger.error(f"Error parsing date format: {error}")
            raise
    
    async def get_photo_download_url(self, photo_id: str) -> str:
        """
        Get a download URL for a specific photo
        
        The returned URL can be used to download the full-resolution photo.
        Note: URLs expire after approximately 1 hour for security reasons.
        
        Args:
            photo_id: Unique ID of the photo (obtained from get_photos or search_photos)
            
        Returns:
            str: Download URL for the photo
            
        Raises:
            HttpError: If the API call fails (e.g., photo not found, no permission)
        """
        try:
            # Get photo metadata including base URL
            photo = self.photos_service.mediaItems().get(mediaItemId=photo_id).execute()
            
            # Construct download URL by adding '=d' parameter to base URL
            # The '=d' parameter tells Google Photos to return the original file for download
            download_url = photo['baseUrl'] + '=d'
            
            logger.info(f"Generated download URL for photo {photo_id}")
            return download_url
            
        except HttpError as error:
            logger.error(f"Error getting download URL for photo {photo_id}: {error}")
            raise