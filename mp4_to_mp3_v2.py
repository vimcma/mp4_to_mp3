from pydub import AudioSegment
import os
import time
from termcolor import colored
import subprocess

os.system('cls')

# Define input and output folders
input_folder = 'mp4'
output_folder = 'mp3'

def extract_audio_with_pydub(mp4_file, output_folder, bitrate):
    print(f"Processing file with pydub: {mp4_file}")
    try:
        # Load the MP4 file
        audio = AudioSegment.from_file(mp4_file, format="mp4")
        # Define the output MP3 file path
        mp3_file = os.path.join(output_folder, os.path.splitext(os.path.basename(mp4_file))[0] + '.mp3')
        # Export the audio as MP3 with the selected bitrate
        audio.export(mp3_file, format="mp3", bitrate=bitrate)
        print(f"Finished processing {mp4_file} -> {mp3_file}")
        mp3_file_size = os.path.getsize(mp3_file)  # Get the size of the mp3 file in bytes
        mp3_file_size_mb = format_file_size(mp3_file_size)  # Convert to MB
        print(colored(f"MP3 file size is {mp3_file_size_mb:.2f} MB", "green"))  # Display size of mp3 in MB
        return mp3_file 
    except Exception as e:
        print(f"\033[91mError processing {mp4_file} with pydub: {e}\033[0m")  # Print error in red
        return None  # Return None in case of an error

def extract_audio_with_ffmpeg(mp4_file, output_folder, bitrate):
    print(f"Processing file with ffmpeg: {mp4_file}")
    # Define the output MP3 file path
    mp3_file = os.path.join(output_folder, os.path.splitext(os.path.basename(mp4_file))[0] + '.mp3')
    # Construct the ffmpeg command
    ffmpeg_cmd = f'ffmpeg -i "{mp4_file}" -b:a {bitrate} "{mp3_file}"'
    try:
        # Run the ffmpeg command
        subprocess.run(ffmpeg_cmd, shell=True, check=True)
        print(f"Finished processing {mp4_file} -> {mp3_file}")
        mp3_file_size = os.path.getsize(mp3_file)  # Get the size of the mp3 file in bytes
        mp3_file_size_mb = format_file_size(mp3_file_size)  # Convert to MB
        print(colored(f"MP3 file size is {mp3_file_size_mb:.2f} MB", "green"))  # Display size of mp3 in MB
        return mp3_file
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError processing {mp4_file} with ffmpeg: {e}\033[0m")  # Print error in red
        return None


def select_bitrate():
    # Display menu for user to select audio quality
    print(colored("Select audio quality for conversion (kbps):", "green"))
    print(colored("1. 32 kbps", "yellow"))
    print(colored("2. 48 kbps", "yellow"))
    print(colored("3. 64 kbps", "yellow"))
    print(colored("4. 128 kbps", "yellow"))
    print(colored("5. 192 kbps", "yellow"))
    print(colored("6. To exit the program", "yellow"))
    # Get user input
    choice = input(colored("Enter your choice from 1 to 6 or just Enter for default bitrate (48kbps): ", "cyan"))
    # Map user choice to bitrate
    bitrate_map = {
        '1': '32k',
        '2': '48k',
        '3': '64k',
        '4': '128k',
        '5': '192k',
        '6': 'ex'
    }
    # Validate user input
    if choice == '':  # Check for empty input first
        selected_bitrate = '48k'  # Default bitrate
        os.system('cls')
        print(colored("Default bitrate has been set (48 kbps).", "green"))
    elif choice in bitrate_map:
        if choice == '6':
            exit()
        else:
            selected_bitrate = bitrate_map[choice]
            print(colored(f"You selected {selected_bitrate} bitrate.", "green"))
    else:
        os.system('cls')
        print(colored("Invalid choice. Please try again.", "red"))
        time.sleep(1)
        os.system('cls')
        return select_bitrate()  # Call the function again for a valid input
    return selected_bitrate  # Return the selected bitrate

def format_file_size(size_in_bytes):
    return size_in_bytes / (1024 * 1024)  # Convert bytes to megabytes

# Main program function
def main():
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    # Get the selected bitrate
    selected_bitrate = select_bitrate()
    # Process each MP4 file in the input folder sequentially
    for filename in os.listdir(input_folder):
        if filename.endswith('.mp4'):
            mp4_path = os.path.join(input_folder, filename)
            mp4_file_size = os.path.getsize(mp4_path)  # Get the size of the mp4 file in bytes
            mp4_file_size_mb = format_file_size(mp4_file_size)  # Convert to MB
            print(colored(f"MP4 file size is {mp4_file_size_mb:.2f} MB", "yellow"))  # Display size of mp4 in MB
            
            # Check file size and choose the appropriate extraction method
            if mp4_file_size < 600 * 1024 * 1024:  # Less than 600 MB
                extract_audio_with_pydub(mp4_path, output_folder, selected_bitrate)
            else:  # 600 MB or larger
                extract_audio_with_ffmpeg(mp4_path, output_folder, selected_bitrate)

    print("Audio extraction complete!")

if __name__ == "__main__":
    main()