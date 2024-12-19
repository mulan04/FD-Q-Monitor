#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.audio import SoundLoader  # For sound playback
import os

# Authentication credentials
api_key = "<My-FD-APIkey>"
password = "X"  # Typically, this is 'X' for Freshdesk API

# Base URL
url = "https://aquasecurity.freshdesk.com/api/v2/search/tickets"

# Declare IDs as variables
group_ids = [16000085997, 16000088975, 16000088976, 16000086229, 16000074458]
agent_id = 16000620846   # "Support Team"

# Configurable query interval (in seconds)
QUERY_INTERVAL = 60  # Interval for querying Freshdesk in seconds

# Sound file path
sound_file = "AztecSkullWhistle.wav"

# Construct the query dynamically to return all 'Open' and 'Unassigned' or owned by 'Support Team' tickets
group_query = " OR ".join([f"group_id:{group_id}" for group_id in group_ids])
query = f'"({group_query}) AND status:2 AND (agent_id:null OR agent_id:{agent_id})"'

# URL parameters
params = {"query": query}

# Function to fetch tickets from Freshdesk API
def fetch_tickets():
    try:
        response = requests.get(url, params=params, auth=HTTPBasicAuth(api_key, password))
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            results = data.get('results', [])
            
            # Store the ticket info as a list of tuples (id, subject, severity)
            ticket_info = [
                (record.get('id'), record.get('subject'), record.get('custom_fields', {}).get('severity', 'N/A'))
                for record in results
            ]
        else:
            ticket_info = [("Error", f"{response.status_code} - {response.text}", "N/A")]
    except Exception as e:
        ticket_info = [("Error", str(e), "N/A")]

    return ticket_info

# Kivy UI class
class TicketApp(App):
    def build(self):
        # Create the root FloatLayout
        self.root = FloatLayout()

        # Add a label container to hold dynamic text
        self.ticket_label = Label(
            text="Loading tickets...",
            font_size='20sp',  # Increase font size
            size_hint=(0.9, 0.8),  # Adjust size to leave margins
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign="center",  # Horizontal alignment
            valign="middle",  # Vertical alignment
        )
        self.ticket_label.bind(size=self.ticket_label.setter('text_size'))  # Enable text wrapping

        # Add the label to the root layout
        self.root.add_widget(self.ticket_label)

        # Preload the sound file
        self.sound = SoundLoader.load(sound_file)
        if not self.sound:
            print("Error: Could not load sound file.")

        # Fetch initial data and update the label
        self.refresh_tickets(0)

        # Schedule periodic updates
        Clock.schedule_interval(self.refresh_tickets, QUERY_INTERVAL)

        return self.root

    def refresh_tickets(self, dt):
        # Fetch the latest ticket data
        ticket_info = fetch_tickets()

        # Build the display string with ticket info
        display_text = ""
        for ticket_id, subject, severity in ticket_info:
            display_text += f"ID: {ticket_id}\nSubject: {subject}\nSeverity: {severity}\n\n"

        if not display_text.strip():
            display_text = "No tickets found."

        # Update the label text
        self.ticket_label.text = display_text

        # Play sound if tickets are found
        if ticket_info and ticket_info[0][0] != "Error":  # Non-error results
            if self.sound:
                self.sound.play()

# Run the Kivy app
if __name__ == "__main__":
    # Check if the sound file exists
    if not os.path.exists(sound_file):
        print(f"Error: Sound file '{sound_file}' not found!")
    else:
        TicketApp().run()
