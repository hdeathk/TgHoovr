This script is a Telegram Video Downloader that automates the process of downloading videos from Telegram channels. By providing your Telegram API credentials and the desired channel's username, URL, or ID, the script fetches all available videos and saves them to a local folder. It features: - Automatic duplicate detection to avoid re-downloading videos. - A customizable maximum number of simultaneous downloads. - Simple configuration with saved API credentials for repeated use. - Progress tracking with a user-friendly interface.

Ideal for managing and archiving videos from Telegram channels efficiently! This guide will walk you through the process from account setup to running the script.

**Step 1: Download the Script**

    git clone https://github.com/hdeathk/TgHoovr

Navigate to the project folder:

    cd TgHoovr

**Step 2: Required Libraries**
Install Required Libraries Use the requirements.txt file to install the dependencies:

    pip install -r requirements.txt

**Step 3: Create a Telegram API Account**
Go to the Telegram API Tools page:

    https://my.telegram.org/auth

Log in Enter your phone number and the verification code sent to your Telegram app.

Create a New Application Go to the "API Development Tools" section. Fill in the required details (e.g., app name, description). Save the API ID and API Hash generated for your application.

**Step 4: Configure the Script**
Run the script:

    python TgHoovr.py

Enter the following when prompted: Your API ID. Your API Hash.

The script will save your configuration in a config.json file for future use.

**Step 5: Download Telegram Videos**

Choose Option 1 to start downloading videos.

Enter the Telegram channel username, URL, or ID. Example formats: channelusername https://t.me/channelusername 1234567890 (Channel ID)*

The script will: Fetch videos from the channel. Download them to a folder named after the channel.

**Step 6: Manage Downloads**

Avoid Duplicate Downloads: The script keeps track of downloaded videos in a downloaded_ids.txt file.

View Logs: Errors and activity logs are stored in downloader.log for troubleshooting.

Optional Customizations
Change Max Downloads: Edit the MAX_SIMULTANEOUS_DOWNLOADS variable in the script to adjust the number of simultaneous downloads.

Reset Credentials: Delete the config.json file and re-run the script to re-enter your API ID and API Hash.

You're Ready to Go!

Start downloading Telegram videos easily by following this guide. For questions or troubleshooting, refer to the logs or contact the repository owner. 🎉
