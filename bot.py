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

# Emoji-Zuordnungstabelle
emojis = {
    "shroom": "🍄", "apple": "🍎", "fish": "🐟", "shower": "🚿",
    "tea": "🍵", "beer": "🍺", "shield": "🛡️", "insurance": "📜",
    "Midnight Meow": "🌜😺", "Pixel Pal": "🎮🐾", "Bunny Buddy": "🐰",
    "Fortune Feline Mask": "🎭🐱", "Baby Yoda Mask": "👽👶",
    "Psychedelic Bunny Mask": "🌀🐇", "Thuglife Shades": "😎",
    "Panda Peepers": "🐼", "Laser Lenses": "🔴👓", "Twintail Tango Wig": "💃",
    "J-Punk Wig": "🤘", "Bear Buddy Beanie": "🧸"
}

# Funktion zum Abrufen der Item-Namen von der API
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

# Abrufen der Item-Namen beim Start des Bots
item_id_to_name_map = fetch_item_names()

# Funktion zur Umwandlung von Item-IDs in Namen mit Emojis oder "X" für bestimmte Items
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

# Funktion zum Abrufen von Pet-Daten
def get_pet_data(pet_id):
    url = "https://api.frenpet.dievardump.com"
    query = f"""
    query {{
        pet(id: {pet_id}) {{
            id
            name
            status
            scoreInt
            level
            timeUntilStarving
            lastAttacked
            lastAttackUsed
            owner
            rewardsInt
            dna
            itemsOwned {{
                id
                petId
                owned
                itemEquipExpires
                updatedAt
            }}
        }}
    }}
    """
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        json_data = response.json()
        if 'data' in json_data and 'pet' in json_data['data']:
            return json_data
        else:
            print("Error in API response:", json_data)
            return None
    else:
        print(f"API request failed with status code {response.status_code}: {response.text}")
        return None

# Funktion zur Formatierung von Pet-Daten
def format_pet_data(pet_data, user_timezone):
    # Definieren Sie die Schlüssel, die Sie anzeigen möchten
    keys_to_display = ['id', 'name', 'status', 'scoreInt', 'level', 
                       'timeUntilStarving', 'lastAttacked', 'lastAttackUsed', 
                       'owner', 'rewardsInt', 'dna']

    formatted_data = []
    for key in keys_to_display:
        value = pet_data.get(key, 'N/A')

        # Formatieren Sie Zeitstempel und Zahlenwerte
        if key in ['lastAttacked', 'lastAttackUsed', 'timeUntilStarving']:
            value = datetime.fromtimestamp(int(value), tz=user_timezone).strftime('%Y-%m-%d %H:%M:%S')
        elif key == 'scoreInt':
            value = f"{int(value) / (10 ** 12):.2f}"
        elif key == 'rewardsInt':
            value = f"{int(value) / (10 ** 18):.2f} ETH"

        formatted_data.append(f"{key.capitalize()}: {value}")

    return "\n".join(formatted_data)

# Hilfsfunktion zur Formatierung der Zeitdifferenz
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

# Slash-Befehl für Pet-Daten
@bot.slash_command(name="pet", description="Get pet data")
async def pet(interaction: Interaction, pet_id: int = SlashOption(description="ID of the pet")):
    user_timezone = timezone.utc  # Setzen Sie hier die Zeitzone des Nutzers
    try:
        pet_data_response = get_pet_data(pet_id)
        if pet_data_response and 'data' in pet_data_response and 'pet' in pet_data_response['data']:
            pet_data = pet_data_response['data']['pet']
            formatted_message = format_pet_data(pet_data, user_timezone)
            await interaction.response.send_message(formatted_message, ephemeral=True)
        else:
            await interaction.response.send_message("There was an error fetching the pet data.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Start the bot with token

bot.run("") 

