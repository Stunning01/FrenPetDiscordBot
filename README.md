# FrenPet Discord Bot

## Overview
The FrenPet Discord Bot is a comprehensive and dynamic tool designed for Discord users who are enthusiasts of the FrenPet game. Built with Python using the Nextcord library, this bot provides an interactive platform to access and manage virtual pet data directly from Discord.

## Key Features
- Direct integration with FrenPet's API for real-time pet data retrieval.
- Custom emoji responses for a fun and engaging user experience.
- Easy-to-use Slash commands for quick access to pet information.
- Detailed display of pet stats including levels, status, and owner information.

## Prerequisites
Before you begin, ensure you have the following:
- Python 3.8 or higher installed on your system.
- A Discord account and a server where you can add the bot.

## Installation Guide

### Step 1: Clone the Repository
- Clone this repository to your local machine using:

git clone https://github.com/yourusername/FrenPetDiscordBot.git

markdown


### Step 2: Install Dependencies
- Navigate to your project directory and install the necessary Python libraries. Your `requirements.txt` should include:


nextcord
requests
python-dotenv
aiohttp

arduino

- To install these, run:

pip install -r requirements.txt


### Step 3: Bot Configuration
- Create a `.env` file in your project directory.
- Add your Discord Bot Token in this file:


BOT_TOKEN=your_discord_bot_token_here

- This step is crucial for securing your bot's token.

### Step 4: Run the Bot
- Execute the bot script with the following command:

python bot.py


## Using the Bot
Once the bot is running on your Discord server, you can use the following commands:
- `/pet [pet_id]`: Retrieves detailed information about a specific pet.

## Contributing
Your contributions are what make the community great. Whether it's bug fixes, feature ideas, or code contributions, feel free to fork this repository, make your changes, and submit a pull request. For bugs or feature requests, please open an issue in the GitHub repository.

## License
This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file.
