import json
from dataclasses import dataclass

import PyChromeDevTools as pychromedevtools


# Define the data class
@dataclass
class Item:
  sport_league: str = ''
  event_date_utc: str = ''
  team1: str = ''
  team2: str = ''
  pitcher: str = ''
  period: str = ''
  line_type: str = ''
  price: str = ''
  side: str = ''
  team: str = ''
  spread: float = 0.0


# Create a function to parse the loaded data and output JSON
def parse_and_output(data):
  
  items = [Item(**item) for item in data]

  
  json_output = json.dumps([item.__dict__ for item in items], indent=2)

  
  print(json_output)


# Connect to Chrome with PyChromeDevTools
chrome = pychromedevtools()

# Open a new tab
chrome.Page.enable()
chrome.Page.navigate(url='https://veri.bet')

# Wait for the page to load
chrome.wait(10)

# Click on 'Access Betting Simulator'
chrome.Input.enable()
chrome.Input.dispatchKeyEvent(type='keyDown', key='Tab')
chrome.Input.dispatchKeyEvent(type='keyUp', key='Tab')
chrome.Input.dispatchKeyEvent(type='keyDown', key='Enter')
chrome.Input.dispatchKeyEvent(type='keyUp', key='Enter')

# Wait for all the data to load 
chrome.wait(20)

# Execute JavaScript to extract data
result = chrome.Runtime.evaluate(expression='''
        // JavaScript extraction logic
const rawData = your_extraction_script();

// Assuming rawData contains the HTML structure of the page
const parser = new DOMParser();
const doc = parser.parseFromString(rawData, 'text/html');

// Extracting data from the page
const eventsContainer = doc.querySelector('.container'); // Adjust this selector based on the actual structure
const events = eventsContainer.querySelectorAll('.row'); // Assuming each event is within a row

// Create an array to store extracted data
const extractedData = [];

events.forEach((event) => {
  const sportLeague = event.querySelector('.btn-primary').innerText.trim();
  const teams = event.querySelectorAll('.btn-primary.btn-sm');
  const team1 = teams[0].innerText.trim();
  const team2 = teams[1].innerText.trim();

  // Extract other information as needed...

  // Create an object for each event
  const eventData = {
    sport_league: sportLeague,
    team1: team1,
    team2: team2,
    // Add other properties based on the structure of the page
  };

  extractedData.push(eventData);
});

// Log the extracted data to the console
console.log(extractedData);

    ''')

# Parse and output the data
parse_and_output(json.loads(result['result']['value']))

# Close the Chrome instance
chrome.close_tab()
chrome.close()
