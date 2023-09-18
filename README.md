# censys-scraper
scrapes services.http.response.body from Censys search results

Usage:

Make a free account at censys.io to access the API.

python censys-scraper.py API_ID SECRET TARGET_STRING SHIFT_LEFT LENGTH

This searches for all response bodies that contain TARGET_STRING as a substring, shifts the cursor left by SHIFT_LEFT from where TARGET_STRING begins, then extracts the following LENGTH characters.
SHIFT_LEFT is useful for finding strings that contain TARGET_STRING as a substring at a fixed offset from the beginning and then extracting the whole string.
To extract strings that start with a specific string, set SHIFT_LEFT to 0, TARGET_STRING to the string to search for, and LENGTH to the length of desired string.
