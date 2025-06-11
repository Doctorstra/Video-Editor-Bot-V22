import subprocess

def merge_videos(input_files, output_path):
    with open("inputs.txt", "w") as f:
        for fpath in input_files:
            f.write(f"file '{fpath}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "inputs.txt", "-c", "copy", output_path],
        check=True
    )
