import IP2Location
import sys
import os
import time
from collections import Counter

# Function to get country from an IP address using IP2Location LITE database
def get_country(ip, db):
    try:
        record = db.get_all(ip)
        return record.country_long  # Returns the country name
    except Exception as e:
        print(f"Error retrieving country for IP {ip}: {e}")
        return None

# Function to display progress
def display_progress(total, current):
    percent = (current / total) * 100
    bar_length = 50  # Length of the progress bar
    filled_length = int(bar_length * percent // 100)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)  # Change to '-' for unfilled part
    print(f"\rScanned: ({bar}) {percent:.2f}% done ({current}/{total})", end='')

# Function to clear the screen
def clear_screen():
    # Clear the console using os.system
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to format country names to fit within a specified width
def format_country_name(country_name, width=30):
    if len(country_name) > width:
        return country_name[:width - 4] + "... "  # Truncate and append "..."
    return country_name.ljust(width)  # Pad with spaces if shorter

# Main function to read IPs from file and count countries
def main(filename, db_path='IP2LOCATION-LITE-DB1.BIN'):
    # Load the IP2Location database
    db = IP2Location.IP2Location(db_path)

    try:
        with open(filename, 'r') as file:
            ips = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File {filename} not found.")
        sys.exit(1)

    total_ips = len(ips)
    countries = Counter()  # Using Counter to manage country counts

    print(f"Loaded: {filename}\n")

    last_update_time = time.time()  # Track the last update time

    for idx, ip in enumerate(ips):
        country = get_country(ip, db)
        if country:
            countries[country] += 1  # Increment the count for the found country

        # Update progress
        display_progress(total_ips, idx + 1)

        # Check if 0.3 seconds have passed for updating the display
        current_time = time.time()
        if current_time - last_update_time >= 0.3:  # Update every 0.3 seconds
            last_update_time = current_time
            
            # Clear the screen and display current counts sorted downwards
            clear_screen()
            print("Current Counts (Top 10 Countries):\n")
            # Sort countries by counts (most IPs at the top)
            sorted_countries = sorted(countries.items(), key=lambda item: item[1], reverse=True)[:10]  # Top 10
            
            total_counted = sum(count for _, count in sorted_countries)  # Total of the top 10
            other_count = sum(countries.values()) - total_counted  # Count for OTHER category

            for country, count in sorted_countries:
                print(f"{format_country_name(country)}: {count} IPs")  # Removed parentheses around count

            # Print the OTHER category on a separate line if applicable
            if other_count > 0:  # Show OTHER only if there are remaining IP
                print(f"\n{format_country_name('OTHER')}: {other_count} IPs\n")  # Removed parentheses around count

    # Clear the screen before showing the final results
    clear_screen()

    # Print sorted country counts for final output (Top 10 + OTHER)
    print("Final Counts (Top 10 Countries):\n")
    sorted_countries = sorted(countries.items(), key=lambda item: item[1], reverse=True)[:10]  # Top 10
    total_counted = sum(count for _, count in sorted_countries)  # Total of the top 10
    other_count = sum(countries.values()) - total_counted  # Count for OTHER category

    for country, count in sorted_countries:
        print(f"{format_country_name(country)}: {count} IPs")  # Removed parentheses around count

    # Print the OTHER category on a separate line if applicable
    if other_count > 0:  # Show OTHER only if there are remaining IP
        print(f"{format_country_name('OTHER')}: {other_count} IPs\n")  # Removed parentheses around count

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py ips.txt")
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)
