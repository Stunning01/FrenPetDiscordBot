import os
import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from datetime import datetime, timezone

# Enable all necessary Intents for the bot
intents = nextcord.Intents.all()

# Create a bot instance with specified intents and changed prefix
bot = commands.Bot(command_prefix='/', intents=intents)

# Emoji Mapping Table
emojis = {
    "shroom": "🍄", "apple": "🍎", "fish": "🐟", "shower": "🚿",
    "tea": "🍵", "beer": "🍺", "shield": "🛡️", "insurance": "📜",
    "Midnight Meow": "🌜😺", "Pixel Pal": "🎮🐾", "Bunny Buddy": "🐰",
    "Fortune Feline Mask": "🎭🐱", "Baby Yoda Mask": "👽👶",
    "Psychedelic Bunny Mask": "🌀🐇", "Thuglife Shades": "😎",
    "Panda Peepers": "🐼", "Laser Lenses": "🔴👓", "Twintail Tango Wig": "💃",
    "J-Punk Wig": "🤘", "Bear Buddy Beanie": "🧸"
    # Add more emoji mappings here
}

# Function to fetch item names from the API
def fetch_item_names():
    url = "https://api.frenpet.dievardump.com"
    query = """
    query {
        items {
            id
            name
        }
    }
    """

    response = requests.post(url, json={'query': query})
    if response.status_code == 200 and 'data' in response.json():
        items = response.json()['data']['items']
        return {item['id']: item['name'] for item in items}
    else:
        print(f"Error: {response.status_code}")
        return {}

# Fetch item names on bot startup
item_id_to_name_map = fetch_item_names()

# Function to convert item IDs to names with emojis or "X" for certain items
def convert_item_ids_to_names_with_check(item_names):
    display_items = {'shield', 'Midnight Meow', 'Pixel Pal', 'Bunny Buddy', 'Fortune Feline Mask',
                     'Baby Yoda Mask', 'Psychedelic Bunny Mask', 'Thuglife Shades', 'Panda Peepers',
                     'Laser Lenses', 'Twintail Tango Wig', 'J-Punk Wig', 'Bear Buddy Beanie'}
    result = []
    for item_name in display_items:
        emoji = emojis.get(item_name, '❓')
        if item_name in item_names:
            result.append(f"{item_name.capitalize()}: {emoji}")
        else:
            result.append(f"{item_name.capitalize()}: ❌")
    return result

# Function to fetch pet data
def get_pet_data(pet_id):
    url = "https://api.frenpet.dievardump.com"
    query = f"""
    query {{
        pet(id: {pet_id}) {{
            id
            name
            status
            score
            level
            timeUntilStarving
            lastAttacked
            lastAttackUsed
            owner
            rewards
            dna
            itemsOwned
            createdAt
        }}
    }}
    """

    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to format pet data
def format_pet_data(pet_data, user_timezone):
    formatted_data = []
    owned_item_ids = set(pet_data.get('itemsOwned', []))
    owned_item_names = [item_id_to_name_map.get(item_id, 'Unknown Item') for item_id in owned_item_ids]

    # Basic data (without status)
    basic_keys = ['id', 'name', 'level', 'score', 'rewards', 'owner']
    for key in basic_keys:
        value = pet_data.get(key)
        if key == 'score':
            value = f"{int(value) / (10 ** 12):.2f}"
        elif key == 'rewards':
            value = f"{int(value) / (10 ** 18):.2f} ETH"
        formatted_data.append(f"{key.capitalize()}: {value}")

    # Time-related data
    time_keys = ['timeUntilStarving', 'lastAttacked', 'lastAttackUsed']
    for key in time_keys:
        value = pet_data.get(key)
        time_diff = datetime.now(user_timezone) - datetime.fromtimestamp(int(value), tz=user_timezone)
        formatted_data.append(f"{key.replace('last', '').capitalize()}: {format_time_diff(time_diff)} ago")

    # Items
    item_display = convert_item_ids_to_names_with_check(owned_item_names)
    formatted_data.extend(item_display)

    # CreatedAt in international format
    created_at = datetime.fromtimestamp(int(pet_data.get('createdAt')), tz=user_timezone).strftime('%Y-%m-%d %H:%M:%S')
    formatted_data.append(f"Created at: {created_at}")

    # DNA
    formatted_data.append(f"DNA: {pet_data.get('dna')}")

    return "\n".join(formatted_data)

# Emoji for keys
def emoji_for_key(key):
    emojis = {
        "id": "🆔",
        "name": "📛",
        "status": "📊",
        "level": "🌟",
        # Add more mappings
    }
    return emojis.get(key, "🔸")

# Helper function to format time difference
def format_time_diff(time_diff):
    days, seconds = time_diff.days, time_diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return f"{days} days"
    elif hours > 0:
        return f"{hours}hr"
    else:
        return f"{minutes}mins"

# Slash command for pet data
@bot.slash_command(name="pet", description="Get pet data")
async def pet(interaction: Interaction, pet_id: int = SlashOption(description="ID of the pet")):
    user_timezone = timezone.utc  # Set the user's timezone here
    try:
        pet_data_response = get_pet_data(pet_id)
        if pet_data_response and 'data' in pet_data_response and 'pet' in pet_data_response['data']:
            pet_data = pet_data_response['data']['pet']
            formatted_message = format_pet_data(pet_data, user_timezone)
            message = formatted_message
        else:
            message = "There was an error fetching the pet data."
        await interaction.response.send_message(message, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

# Event called when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Start the bot with the given token
bot.run("Your Bot Token")
