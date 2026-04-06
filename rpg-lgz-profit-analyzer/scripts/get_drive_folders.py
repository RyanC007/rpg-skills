"""
get_drive_folders.py
--------------------
Queries the Logoclothz shared Google Drive orders folder and builds
a JSON map of {folder_name: drive_url}.

The shared folder ID is hardcoded — it is the ALL ORDERS folder at:
https://drive.google.com/drive/folders/1q0HmZJjj_hXkurMn-HehYe5dbcKZbxut

Output: /tmp/drive_folder_map.json
"""

import subprocess
import json

DRIVE_FOLDER_ID = '1q0HmZJjj_hXkurMn-HehYe5dbcKZbxut'
RCLONE_CONFIG   = '/home/ubuntu/.gdrive-rclone.ini'
OUTPUT_PATH     = '/tmp/drive_folder_map.json'

print(f"Querying Google Drive folder: {DRIVE_FOLDER_ID}")
print("This may take 30-60 seconds for large folders...")

result = subprocess.run(
    [
        'rclone', 'lsjson',
        'manus_google_drive:',
        '--config', RCLONE_CONFIG,
        '--dirs-only',
        f'--drive-root-folder-id={DRIVE_FOLDER_ID}',
    ],
    capture_output=True, text=True, timeout=180
)

if result.returncode != 0:
    print(f"ERROR: rclone failed: {result.stderr}")
    exit(1)

folders = json.loads(result.stdout)
folder_map = {
    f['Name'].upper(): f'https://drive.google.com/drive/folders/{f["ID"]}'
    for f in folders
}

with open(OUTPUT_PATH, 'w') as out:
    json.dump(folder_map, out, indent=2)

print(f"Found {len(folder_map)} folders.")
print(f"Saved to {OUTPUT_PATH}")
