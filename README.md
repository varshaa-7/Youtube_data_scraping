# YouTube Channel Insights Script

This Python script uses the **YouTube Data API v3** to fetch and display details about a specific YouTube channel and its recent video uploads. It provides insights such as video titles, view counts, like counts, durations, hashtags used, and more.

## Features

- Fetches basic channel information: Title, Verification status, Subscriber count.
- Retrieves the 10 most recent uploaded videos.
- Displays detailed stats for each video:
  - Title
  - Publish date
  - Duration
  - View count
  - Like count
  - Comment count
  - Hashtags in description
  - Video URL

## Requirements

- Python 3.6+
- Internet connection
- YouTube Data API v3 key

## Setup

1. **Clone this repository or download `file7.py`**

2. **Install required Python packages** (if not already installed):
   ```bash
   pip install requests
