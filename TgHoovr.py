import asyncio
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterVideo
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from tqdm import tqdm
import os
import logging
from logging.handlers import RotatingFileHandler
import time
from threading import Thread
import json
import re

# ASCII banner configuration
def get_banner():
    return """
$$$$$$$$\\        $$\\   $$\\                                         
\\__$$  __|       $$ |  $$ |                                        
   $$ | $$$$$$\\  $$ |  $$ | $$$$$$\\   $$$$$$\\ $$\\    $$\\  $$$$$$\\  
   $$ |$$  __$$\\ $$$$$$$$ |$$  __$$\\ $$  __$$\\\\$$\\  $$  |$$  __$$\\ 
   $$ |$$ /  $$ |$$  __$$ |$$ /  $$ |$$ /  $$ |\\$$\\$$  / $$ |  \\__|
   $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ | \\$$$  /  $$ |      
   $$ |\\$$$$$$$ |$$ |  $$ |\\$$$$$$  |\\$$$$$$  |  \\$  /   $$ |      
   \\__| \\____$$ |\\__|  \\__| \\______/  \\______/    \\_/    \\__|      
       $$\\   $$ |                                                  
       \\$$$$$$  |                                                  
        \\______/                                                   
"""

# Global variables
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_PATH, "config.json")
MAX_SIMULTANEOUS_DOWNLOADS = 10

# Configure logging with UTF-8 encoding
LOG_FILE = os.path.join(BASE_PATH, "downloader.log")
handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding='utf-8')
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load or request configuration details
def load_or_request_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            print("Configuration successfully loaded.")
            return config
    else:
        print("No configuration found. Please enter your details:")
        api_id = input("Enter your API ID: ").strip()
        api_hash = input("Enter your API Hash: ").strip()

        config = {
            "api_id": int(api_id),
            "api_hash": api_hash
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False)
        print("Configuration saved.")
        return config

# Load IDs of already downloaded videos
def load_downloaded_ids(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(map(int, file.read().splitlines()))
    return set()

# Save a downloaded ID immediately
def save_downloaded_id(file_path, message_id):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{message_id}\n")
    logging.info(f"ID saved: {message_id}")

# Function to sanitize file/folder names
def sanitize_folder_name(name):
    sanitized = re.sub(r'[<>:"/\\|?*\n\r]+', '_', name)
    return sanitized.strip() or "Unnamed_Channel"

# Function to resolve usernames, IDs, or invite links
async def resolve_channel(client, input_string):
    try:
        if input_string.isdigit():
            channel = await client(GetFullChannelRequest(int(input_string)))
            entity = channel.full_chat
            title = sanitize_folder_name(entity.about or f"Channel_{input_string}")
            return entity, title
        match = re.match(r"(https?://)?(www\.)?(t\.me|telegram\.me)/(\+?[a-zA-Z0-9_+-]+)", input_string)
        if match:
            invite_part = match.group(4)
            if invite_part.startswith('+'):
                result = await client(ImportChatInviteRequest(invite_part[1:]))
                entity = result.chats[0]
            else:
                entity = await client.get_entity(invite_part)
            return entity, sanitize_folder_name(entity.title)
        else:
            entity = await client.get_entity(input_string.strip())
            return entity, sanitize_folder_name(entity.title)
    except Exception as e:
        raise ValueError(f"Unable to resolve the channel: {e}")

# Function to download with smooth progress bar
async def download_video(client, message, folder, position, download_stats):
    try:
        video_bar = tqdm(
            total=message.file.size if message.file else 0,
            unit="B",
            unit_scale=True,
            desc=f"Video {message.id}",
            leave=False,
            position=position,
        )
        total_downloaded = 0

        def progress_callback(current, total):
            nonlocal total_downloaded
            delta = current - total_downloaded
            total_downloaded = current
            download_stats["current_speed"][position] = delta / 0.1
            video_bar.update(delta)

        file_path = await client.download_media(
            message,
            file=os.path.join(folder, f"{message.id}.mp4"),
            progress_callback=progress_callback,
        )
        video_bar.close()

        if file_path and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            size = os.path.getsize(file_path)
            download_stats["total_size"] += size
            logging.info(f"Successfully downloaded: {file_path}")
            return True
        else:
            raise Exception("File validation failed.")
    except Exception as e:
        logging.warning(f"Error downloading video {message.id}: {e}")
        return False

# Main function
async def main(config):
    channel_input = input("Enter the username, URL, or Telegram channel ID: ").strip()

    async with TelegramClient('session_name', config['api_id'], config['api_hash']) as client:
        print("Connecting to client...")
        try:
            channel, folder_name = await resolve_channel(client, channel_input)
            print(f"Accessing channel: {channel.title if hasattr(channel, 'title') else 'Private channel'}")
        except ValueError as e:
            print(f"Error: {e}")
            return

        channel_folder = os.path.join(BASE_PATH, folder_name)
        download_folder = os.path.join(channel_folder, "downloaded")
        downloaded_ids_file = os.path.join(channel_folder, "downloaded_ids.txt")
        os.makedirs(download_folder, exist_ok=True)

        downloaded_ids = load_downloaded_ids(downloaded_ids_file)

        print("Fetching videos...")
        videos = []
        async for message in client.iter_messages(channel, filter=InputMessagesFilterVideo):
            if message.id not in downloaded_ids:
                size = message.file.size if message.file else 0
                videos.append((message, size))

        if not videos:
            print("No videos found or all videos have already been downloaded.")
            return

        videos.sort(key=lambda x: x[1])

        total_bar = tqdm(
            total=len(videos),
            desc="Remaining videos",
            position=MAX_SIMULTANEOUS_DOWNLOADS + 1,
            unit="video",
            leave=True,
        )

        semaphore = asyncio.Semaphore(MAX_SIMULTANEOUS_DOWNLOADS)
        download_stats = {"total_size": 0, "completed": 0, "current_speed": [0] * MAX_SIMULTANEOUS_DOWNLOADS}

        async def worker(video, position):
            async with semaphore:
                message = video[0]
                success = await download_video(client, message, download_folder, position, download_stats)
                if success:
                    save_downloaded_id(downloaded_ids_file, message.id)
                    download_stats["completed"] += 1
                    total_bar.update(1)

        tasks = [worker(video, i % MAX_SIMULTANEOUS_DOWNLOADS) for i, video in enumerate(videos)]
        await asyncio.gather(*tasks)
        total_bar.close()
        print("Download completed.")

# Interactive script
def run_script():
    print(get_banner())
    print("1. Start download")
    print("2. Quit")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        config = load_or_request_config()
        try:
            asyncio.run(main(config))
        except KeyboardInterrupt:
            print("\nInterrupt detected. Saving progress...")
    elif choice == "2":
        print("Goodbye!")
    else:
        print("Invalid option.")
        run_script()

if __name__ == "__main__":
    run_script()
