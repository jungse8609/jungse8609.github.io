
import os
import json
from datetime import datetime, timedelta
import re

def main():
    # --- Configuration ---
    posts_dir = "_posts"
    img_posts_dir = "assets/img/posts"
    settings_file = ".vscode/settings.json"
    months_to_keep = 2
    # --- End Configuration ---

    cutoff_date = datetime.now() - timedelta(days=months_to_keep * 30)
    
    # --- Read settings.json ---
    settings = {}
    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Strip comments before parsing
            content = re.sub(r"//.*", "", content)
            content = re.sub(r"/\*[\s\S]*?\*/", "", content, flags=re.MULTILINE)
            settings = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Could not read or parse {settings_file}: {e}")
        settings = {"files.exclude": {}}

    if "files.exclude" not in settings:
        settings["files.exclude"] = {}

    # --- Remove the general _posts rule if it exists ---
    if "_posts" in settings["files.exclude"]:
        del settings["files.exclude"]["_posts"]

    # --- Find and add old posts to exclude ---
    if os.path.exists(posts_dir):
        for filename in os.listdir(posts_dir):
            try:
                file_date_str = "-".join(filename.split("-")[:3])
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
                if file_date < cutoff_date:
                    settings["files.exclude"][f"{posts_dir}/{filename}"] = True
            except (ValueError, IndexError):
                continue

    # --- Find and add old image folders to exclude ---
    if os.path.exists(img_posts_dir):
        for dirname in os.listdir(img_posts_dir):
            if os.path.isdir(os.path.join(img_posts_dir, dirname)):
                try:
                    dir_date_str = "-".join(dirname.split("-")[:3])
                    dir_date = datetime.strptime(dir_date_str, "%Y-%m-%d")
                    if dir_date < cutoff_date:
                        settings["files.exclude"][f"{img_posts_dir}/{dirname}"] = True
                except (ValueError, IndexError):
                    continue

    # --- Write updated settings.json ---
    try:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        print(f"Successfully updated {settings_file} to hide old files.")
    except IOError as e:
        print(f"Error writing to {settings_file}: {e}")

if __name__ == "__main__":
    main()
