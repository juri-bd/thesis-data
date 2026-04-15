import os
import re

def rename_speakers_in_transcripts():
    """
    Renames generic [SPEAKER_XX] tags to meaningful names.

    Only processes files that do NOT already exist in the final folder.
    If a file with the same name is found in the final directory, it is skipped.
    """
    # --- Configuration ---
    source_dir = "transcription/output"
    final_dir = "transcription/final"

    print("Starting speaker renaming process...")

    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found.")
        return

    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
        print(f"Created final output directory: {final_dir}")

    files_to_process = [f for f in os.listdir(source_dir) if f.endswith(".txt")]

    if not files_to_process:
        print(f"No .txt files found in '{source_dir}'.")
        return

    print(f"Found {len(files_to_process)} transcript(s) to check.")

    speaker_pattern = re.compile(r'(\[SPEAKER_\d+\])')

    for filename in files_to_process:
        source_file_path = os.path.join(source_dir, filename)
        final_file_path = os.path.join(final_dir, filename)

        # Skip if already processed
        if os.path.exists(final_file_path):
            print(f"Skipping '{filename}' (already exists in final folder).")
            continue

        print(f"\n--- Processing file: {filename} ---")

        with open(source_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        unique_speakers = sorted(set(speaker_pattern.findall(content)))

        if not unique_speakers:
            print("No [SPEAKER_XX] tags found. Copying file as is.")
            with open(final_file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
            continue

        print(f"Found speakers: {', '.join(unique_speakers)}")

        speaker_map = {}
        for speaker in unique_speakers:
            while True:
                new_name = input(f"Enter the name for {speaker}: ")
                if new_name.strip():
                    speaker_map[speaker] = new_name.strip()
                    break
                else:
                    print("Name cannot be empty. Please try again.")

        for old_name, new_name in speaker_map.items():
            content = content.replace(old_name, new_name)

        with open(final_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Saved processed file to '{final_file_path}'")

    print("\nAll eligible files have been processed.")


if __name__ == "__main__":
    rename_speakers_in_transcripts()
