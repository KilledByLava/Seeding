import requests
import pyperclip
import pyautogui
import time
import csv

# Constants for the API and Discord
API_URL = 'https://balatro.virtualized.dev:4931/api/'
QUEUE_ID = '1'
DEFAULT_MMR = 200  # Default MMR for players not found in the API


# Function to fetch leaderboard data from NEATQueue API
def fetch_data():
    url = f"{NEATQUEUE_URL}/stats/leaderboard/{QUEUE_ID}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None  # Handle errors gracefully


# Function to load tournament players from a CSV file
def load_tournament_players(csv_filename):
    tournament_players = {}
    try:
        with open(csv_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) < 2:
                    continue  # Skip invalid rows
                player_name, player_id = row[1].rsplit(" (", 1)  # Split name and ID
                player_id = player_id.strip(")")  # Clean up ID
                tournament_players[player_id] = player_name
    except Exception as e:
        print(f"Error reading CSV file: {e}")

    return tournament_players


# Function to copy message to clipboard
def copy_to_clipboard(message):
    pyperclip.copy(message)
    print(f"Message copied to clipboard: {message}")


# Function to simulate pasting and sending the message
def paste_and_send():
    pyautogui.hotkey('ctrl', 'v')  # Paste the clipboard content
    time.sleep(0.5)  # Small delay
    pyautogui.press('enter')  # Press Enter to send


# Function to send leaderboard update commands
def send_seeding_commands(data, tournament_name, tournament_players):
    api_players = {str(player["id"]): round(player["data"].get("mmr", 0), 2) for player in data["alltime"]}

    for player_id, player_name in tournament_players.items():
        mmr = api_players.get(player_id, DEFAULT_MMR)  # Get MMR or assign default

        message = f"/leaderboard edit leaderboard_name: {tournament_name} action: Set Points points: {mmr} player: {player_id}"

        # Copy to clipboard and paste/send
        copy_to_clipboard(message)
        time.sleep(.25)  # Short delay
        paste_and_send()
        time.sleep(.25)  # Delay before next message


# Main function
def main():
    # Fetch leaderboard data
    data = fetch_data()
    if not data or "alltime" not in data:
        print("❌ Error: No leaderboard data found.")
        return

    # Load tournament players from CSV
    csv_filename = input("Enter the CSV filename (including .csv extension): ").strip()
    tournament_players = load_tournament_players(csv_filename)

    # Get tournament name
    tournament_name = input("Enter the tournament name: ").strip()

    print("Switch to Discord — starting in 5 seconds...")
    time.sleep(5)

    # Send seeding commands
    send_seeding_commands(data, tournament_name, tournament_players)

    print(f"✅ Seeding complete for **{tournament_name}**!")


if __name__ == "__main__":
    main()
