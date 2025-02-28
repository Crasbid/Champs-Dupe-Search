import re
import os
from collections import defaultdict

def parse_card_file(filename):
    card_dict = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for line in lines:
        match = re.match(r"(\d+)x\s(.+)", line.strip())
        if match:
            count, card_name = match.groups()
            card_dict[card_name] = int(count)
    
    return card_dict

def process_directory(directory):
    all_cards = defaultdict(list)
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            card_data = parse_card_file(file_path)
            
            for card_name, count in card_data.items():
                all_cards[card_name].append((filename, count))
    
    # Remove entries that only appear in one file
    all_cards = {card: entries for card, entries in all_cards.items() if len(entries) > 1}
    
    return all_cards

def save_card_data(card_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for card_name in sorted(card_data.keys()):
            file.write(f"{card_name}: {card_data[card_name]}\n")

def generate_deck_breakdown(all_cards):
    deck_breakdown = defaultdict(list)
    
    for card_name, entries in all_cards.items():
        for filename, count in entries:
            deck_breakdown[filename].append(f"{count}x {card_name}")
    
    return deck_breakdown

def save_deck_breakdown(deck_breakdown, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for deck, cards in deck_breakdown.items():
            file.write(f"\nDeck: {deck}\n")
            for card in cards:
                file.write(f"{card}\n")

# Example usage:
card_data = process_directory("./card_files")
deck_breakdown = generate_deck_breakdown(card_data)

save_card_data(card_data, "ReUsed_Cards.txt")
save_deck_breakdown(deck_breakdown, "Deck_Beakdown.txt")
