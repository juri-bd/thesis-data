import os
import subprocess
import re

def add_newlines_between_speakers(file_path):
    """
    Reads a transcription file and adds a blank line every time the speaker changes.
    """
    print(f"Formatting {os.path.basename(file_path)} for speaker breaks...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines:
            return # Do nothing if the file is empty

        formatted_lines = []
        last_speaker = None
        # This regex pattern finds the speaker tag, e.g., [SPEAKER_00]
        speaker_pattern = re.compile(r'(\[SPEAKER_\d+\])')

        for line in lines:
            match = speaker_pattern.match(line.strip())
            
            if match:
                current_speaker = match.group(1)
                # If last_speaker has been set and is different from the current one, add a newline
                if last_speaker is not None and current_speaker != last_speaker:
                    formatted_lines.append('\n')
                last_speaker = current_speaker
            
            # Add the original line to our new list
            formatted_lines.append(line)

        # Write the newly formatted content back to the original file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(formatted_lines)
        
        print("Formatting complete.")

    except FileNotFoundError:
        print(f"Error: Could not find file {file_path} to format.")
    except Exception as e:
        print(f"An error occurred during formatting: {e}")


def transcribe_videos():
    """
    Finds and transcribes video files using whisperx, skipping existing ones,
    and then formats the output to have newlines between speakers.
    """
    # --- Configuration ---
    input_dir = "transcription/input"
    output_dir = "transcription/output"
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']

    # --- Script Execution ---
    print("Starting transcription process...")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    files_to_process = [f for f in os.listdir(input_dir) if any(f.lower().endswith(ext) for ext in video_extensions)]

    if not files_to_process:
        print(f"No video files found in '{input_dir}'.")
        return

    print(f"Found {len(files_to_process)} video file(s) to process.")

    for filename in files_to_process:
        base_name = os.path.splitext(filename)[0]
        output_file_path = os.path.join(output_dir, base_name + ".txt")

        if os.path.exists(output_file_path):
            print(f"\nSkipping '{filename}': Transcription already exists.")
            continue

        input_file_path = os.path.join(input_dir, filename)
        
        print(f"\nProcessing: {filename}")

        command = [
            "python", "-m", "whisperx", input_file_path,
            "--model", "large-v3", "--language", "en", "--diarize",
            "--device", "cuda", "--output_format", "txt", "--output_dir", output_dir
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Successfully transcribed {filename}")

            # --- NEW: POST-PROCESS THE FILE TO ADD NEWLINES ---
            add_newlines_between_speakers(output_file_path)

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while processing {filename}: {e}")
        except FileNotFoundError:
            print("Error: 'python' command not found. Make sure Python is in your system's PATH.")
            break

    print("\nTranscription process complete.")


if __name__ == "__main__":
    transcribe_videos()