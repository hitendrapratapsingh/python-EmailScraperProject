import requests
import re
from datetime import datetime

# Better email regex
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

with open("websites.txt", "r") as file:
    websites = file.readlines()

all_emails = []

for site in websites:
    site = site.strip()
    print("Checking:", site)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(site, headers=headers, timeout=10)
        html = response.text

        emails = re.findall(email_pattern, html)

        # re.findall returns tuple because of group (com|in|...)
        raw_matches = re.finditer(email_pattern, html)

        for match in raw_matches:
            email = match.group()
            
            # Skip image files manually (extra safety)
            unwanted_extensions = [
            ".png", ".jpg", ".jpeg", ".webp", ".svg",
            ".gif", ".bmp", ".tiff", ".ico", ".avif",
            ".heic", ".mp4", ".mp3", ".pdf", ".zip"
            ]
            if any(email.lower().endswith(ext) for ext in unwanted_extensions):
                continue
            
            print("Found:", email)
            all_emails.append(email)

    except Exception as e:
        print("Error:", e)

# Remove duplicates and sort
cleaned_emails = sorted(set(all_emails))

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(f"emails_{current_time}.txt", "w") as output:
    for email in cleaned_emails:
        output.write(email + "\n")

print("Finished! Clean emails saved in emails_current_time.txt")
