import yt_dlp
import os
from moviepy.editor import AudioFileClip, concatenate_audioclips
from flask import Flask, request, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

def download_videos(singer_name, num_videos):
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best quality audio
        'noplaylist': True,
        'extract-audio': True,  # Extract only the audio
        # 'audio-format': 'mp3',  # Convert the audio to mp3
        'outtmpl': f'{singer_name}/%(title)s.%(ext)s',  # Save the file as mp3
        'default_search': 'ytsearch',
    }

    # Construct YouTube search query
    search_query = f"{singer_name} songs"

    # Ensure the directory exists
    os.makedirs(singer_name, exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Search for the videos
            results = ydl.extract_info(f"ytsearch{num_videos}:{search_query}", download=False)
            videos = results.get('entries', [])

            if len(videos) == 0:
                print(f"No videos found for {singer_name}.")
                return False

            # Limit the videos to num_videos and start downloading
            for i, video in enumerate(videos[:num_videos]):
                print(f"Downloading video {i + 1}: {video['title']}")
                ydl.download([video['webpage_url']])

        except Exception as e:
            print(f"Error during download: {e}")
            return False

    return True

def process_audio_files(singer_name, duration):
    files_dir = f"{singer_name}"
    audio_clips = []

    # List all downloaded audio files in the directory
    for file_name in os.listdir(files_dir):
        if file_name.endswith(('.mp3', '.webm', '.m4a')):
            try:
                file_path = os.path.join(files_dir, file_name)
                audio_clip = AudioFileClip(file_path)

                if audio_clip.duration < duration:
                    print(f"File {file_name} is shorter than {duration} seconds, using full length.")
                    audio_clips.append(audio_clip)
                else:
                    audio_clips.append(audio_clip.subclip(0, duration))

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    if audio_clips:
        # Concatenate all audio clips
        final_audio = concatenate_audioclips(audio_clips)
        output_file = f"{singer_name}_mashup.mp3"
        final_audio.write_audiofile(output_file)
        print(f"Mashup created: {output_file}")
        return output_file
    else:
        print("No audio clips were found. Cannot create a mashup.")
        return None

def mashup(singer_name, num_videos, duration):
    """
    Main function to create a mashup of the singer's videos.
    """
    download_success = download_videos(singer_name, num_videos)
    if not download_success:
        print("Failed to download videos or no videos found.")
        return None
    return process_audio_files(singer_name, duration)

def send_email_with_attachment(receiver_email, file_path):
    sender_email = "ssoumya_be22@thapar.edu"
    sender_password = "Sjindal_13"

    subject = "Your Mashup"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the file
    part = MIMEBase('application', "octet-stream")
    with open(file_path, "rb") as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
    msg.attach(part)

    # Send the email via Gmail's SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent to {receiver_email} with attachment {file_path}")
    except Exception as e:
        print(f"Error sending email: {e}")


@app.route('/')
def index():
    return render_template('mashup.html')

@app.route('/mashup', methods=['POST'])
def mashup_route():
    # Extract data from form submission
    singer_name = request.form['singer_name']
    num_videos = int(request.form['num_videos'])
    duration = int(request.form['duration'])
    receiver_email = request.form['email']

    # Create mashup
    mashup(singer_name, num_videos, duration)

    # Define the path to the mashup file
    mashup_file_path = f"{singer_name}_mashup.mp3"

    # Send the email with the mashup file attached
    send_email_with_attachment(receiver_email, mashup_file_path)

    return "Mashup created and emailed successfully!"


if __name__ == '__main__':
    app.run(debug=True)


