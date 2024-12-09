#### **🎥 Telegram Video Downloader Script**

This script automates the process of downloading videos from Telegram channels. By providing your Telegram API credentials and the desired channel's username, URL, or ID, the script fetches all available videos and saves them to a local folder.  
  
&nbsp;&nbsp;&nbsp;&nbsp;✨ Features  
&nbsp;&nbsp;&nbsp;&nbsp;🛡️ Automatic duplicate detection to avoid re-downloading videos.  
&nbsp;&nbsp;&nbsp;&nbsp;⚡ Customizable simultaneous downloads for optimized performance.  
&nbsp;&nbsp;&nbsp;&nbsp;🔒 Simple configuration with saved API credentials for ease of use.  
&nbsp;&nbsp;&nbsp;&nbsp;📊 Progress tracking with a user-friendly interface.  
<br>
<br>
<font size="20"> **📋 Step-by-Step Guide**</font>  

  
  
#### **Step 1: Download the Script**

Clone the repository:

    git clone https://github.com/hdeathk/TgHoovr

Navigate to the project folder:

    cd TgHoovr



#### **Step 2: Install Required Libraries**

Install all necessary libraries using the requirements.txt file:

    pip install -r requirements.txt



#### **Step 3: Create a Telegram API Account**

Visit the Telegram API Tools page.
                
    https://my.telegram.org/auth

   Log in using your phone number and the verification code sent to your Telegram app.
   Create a new application:
        Fill in details like App Name and Description.
        Save the API ID and API Hash for later use.

#### **Step 4: Configure the Script**

Run the script for the first time:

    python TgHoovr.py

When prompted, enter:
Your API ID  
Your API Hash  

(The script will save this information in a config.json file for future use.)

#### **Step 5: Download Telegram Videos**

Run the script and choose Option 1 from the menu.
Enter the Telegram channel's username, URL, or ID in one of these formats:
        channelusername
        https://t.me/channelusername
        1234567890 (Channel ID)

**📥 What happens next:**
The script fetches videos from the specified channel.  
All videos are downloaded to a folder named after the channel.

**🔧 Managing Downloads**
Avoid Duplicate Downloads:
The script tracks downloaded videos in a downloaded_ids.txt file.

View Logs:
Errors and activity logs are saved in downloader.log for easy troubleshooting.

**⚙️ Optional Customizations**

Change Maximum Downloads:
Edit the MAX_SIMULTANEOUS_DOWNLOADS variable in the script to adjust the number of simultaneous downloads.

Reset Credentials:
Delete the config.json file and re-run the script to re-enter your API ID and API Hash.

**🚀 Ready to Go!**

🎉 Enjoy your seamless video management!
