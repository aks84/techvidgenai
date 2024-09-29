import subprocess

def start_recording(os_type):
    if os_type == 'macOS':
        command = "ffmpeg -f avfoundation -framerate 30 -i 1 -r 30 -y output_macOS.mp4"
    elif os_type == 'Windows':
        command = "ffmpeg -f gdigrab -framerate 30 -i desktop -y output_windows.mp4"
    elif os_type == 'Ubuntu':
        command = "ffmpeg -f x11grab -framerate 30 -i :0.0 -y output_ubuntu.mp4"
    else:
        return None

    subprocess.run(command, shell=True)
    return f"output_{os_type}.mp4"
