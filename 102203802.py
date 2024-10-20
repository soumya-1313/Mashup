# from flask import Flask, render_template, request, jsonify
# import os
# from pytube import Search, YouTube
# from moviepy.editor import VideoFileClip
# from pydub import AudioSegment
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders

# app = Flask(__name__)

# # Step 1: Download N videos from YouTube
# def download_videos(singer_name, num_videos, download_folder='videos/'):
#     if not os.path.exists(download_folder):
#         os.makedirs(download_folder)
        
#     search = Search(singer_name)
#     for i in range(min(num_videos, len(search.results))):
#         video = search.results[i]
#         yt = YouTube(video.watch_url)
        
#         stream = yt.streams.filter(only_audio=True).first()
#         stream.download(output_path=download_folder, filename=f'{singer_name}_{i}.mp4')

# # Step 2: Convert to audio
# def convert_to_audio(video_folder, audio_folder='audios/'):
#     if not os.path.exists(audio_folder):
#         os.makedirs(audio_folder)
    
#     for video_file in os.listdir(video_folder):
#         if video_file.endswith('.mp3'):
#             video_path = os.path.join(video_folder, video_file)
#             audio_output = os.path.join(audio_folder, video_file.replace('.mp4', '.mp3'))
            
#             clip = VideoFileClip(video_path)
#             clip.audio.write_audiofile(audio_output)

# # Step 3: Trim the first Y seconds of each audio file
# def trim_audio_files(audio_folder, trim_time_sec, trimmed_folder='trimmed_audios/'):
#     if not os.path.exists(trimmed_folder):
#         os.makedirs(trimmed_folder)
    
#     for audio_file in os.listdir(audio_folder):
#         if audio_file.endswith('.mp3'):
#             audio_path = os.path.join(audio_folder, audio_file)
#             output_path = os.path.join(trimmed_folder, audio_file)
            
#             audio = AudioSegment.from_file(audio_path)
#             trimmed_audio = audio[:trim_time_sec * 1000]  # First Y seconds
#             trimmed_audio.export(output_path, format="mp3")

# # Step 4: Merge all audios into one output file
# def merge_audios(trimmed_folder, output_file='final_output.mp3'):
#     combined = AudioSegment.empty()
    
#     for trimmed_file in os.listdir(trimmed_folder):
#         if trimmed_file.endswith('.mp3'):
#             trimmed_audio_path = os.path.join(trimmed_folder, trimmed_file)
#             audio = AudioSegment.from_file(trimmed_audio_path)
#             combined += audio
    
#     combined.export(output_file, format="mp3")

# # Send email with the final file
# def send_email(receiver_email, attachment):
#     sender_email = "ssoumya_be22@thapar.edu"
#     password = "Sjindal_13"

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = "Your Mashup is Ready"

#     # Attach the file
#     part = MIMEBase('application', 'octet-stream')
#     part.set_payload(open(attachment, 'rb').read())
#     encoders.encode_base64(part)
#     part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
#     msg.attach(part)

#     # Send email
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(sender_email, password)
#         server.send_message(msg)


# @app.route('/')
# def index():
#     return render_template('mashup.html')

# @app.route('/mashup', methods=['POST'])
# def mashup():
#     singer_name = request.form['singer_name']
#     num_videos = int(request.form['num_videos'])
#     duration = int(request.form['duration'])
#     email = request.form['email']
    
#     # Run the mashup creation steps
#     download_videos(singer_name, num_videos)
#     convert_to_audio('videos/')
#     trim_audio_files('audios/', duration)
#     merge_audios('trimmed_audios/', output_file='final_output.mp3')
    
#     # Send the final mashup via email
#     send_email(email, 'final_output.mp3')
    
#     return jsonify({"message": "Mashup created and sent to your email!"})

# if __name__ == "__main__":
#     app.run(debug=True)


# import yt_dlp
# import os
# from moviepy.editor import AudioFileClip, concatenate_audioclips
# from flask import Flask, request, render_template
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders

# app = Flask(__name__)

# def download_videos(singer_name, num_videos):
   
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'noplaylist': True,
#         'extract-audio': True,
#         'audio-format': 'mp3',
#         'outtmpl': f'{singer_name}/%(title)s.%(ext)s',
#         'default_search': 'ytsearch',
#         # 'max_downloads': num_videos,
#     }
#     # Construct YouTube search URL (or you can use YouTube Data API to fetch links)
#     search_query = f"{singer_name} songs"

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         # ydl.download([search_query])
#         results = ydl.extract_info(f"ytsearch{num_videos}:{search_query}", download=False)
#         videos = results['entries']

#         if len(videos) < num_videos:
#             print(f"Only found {len(videos)} videos for {singer_name}.")
        
#         for i, video in enumerate(videos[:num_videos]):
#             video_url = video['url']
#             print(f"Downloading video {i+1}: {video_url}")
#             ydl.download([video_url])

# print(f"Files in {singer_name}: {os.listdir(singer_name)}")

# def process_audio_files(singer_name, duration):

#     files_dir = f"{singer_name}"
#     audio_clips = []

#     # List all downloaded files in the directory
#     for file_name in os.listdir(files_dir):
#         if file_name.endswith('.mp3'):
#             try:
#                 audio_clip = AudioFileClip(os.path.join(files_dir, file_name)).subclip(0, duration)
#                 audio_clips.append(audio_clip)

#                 if audio_clip.duration < duration:
#                     print(f"File {file_name} is shorter than {duration}s. Using full length.")
#                     audio_clips.append(audio_clip)
#                 else:
#                     audio_clips.append(audio_clip.subclip(0, duration))
#             except Exception as e:
#                 print(f"Error processing {file_name}: {e}")
            

#     if audio_clips:
#         # Concatenate all audio clips
#         final_audio = concatenate_audioclips(audio_clips)
#         final_audio.write_audiofile(f"{singer_name}_mashup.mp3")
#         print(f"Mashup created: {singer_name}_mashup.mp3")
#     else:
#         print("No audio clips were found. Cannot create a mashup.")
    
# def mashup(singer_name, num_videos, duration):
#     """
#     Main function to create a mashup of the singer's videos.
#     """
#     download_videos(singer_name, num_videos)
#     process_audio_files(singer_name, duration)

# from flask import Flask, request, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('mashup.html')

# @app.route('/mashup', methods=['POST'])
# def mashup_route():
#     # Extract data from form submission
#     singer_name = request.form['singer_name']
#     num_videos = int(request.form['num_videos'])
#     duration = int(request.form['duration'])

#     # Create mashup
#     mashup(singer_name, num_videos, duration)

#     return "Mashup created successfully!"

# def send_email_with_attachment(receiver_email, file_path):
#     sender_email = "ssoumya_ne22@thapar.edu"
#     sender_password = "Sjindal_13"

#     subject = "Your Mashup"
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     # Attach the file
#     part = MIMEBase('application', "octet-stream")
#     part.set_payload(open(file_path, "rb").read())
#     encoders.encode_base64(part)
#     part.add_header('Content-Disposition', 'attachment; filename="mashup.mp3"')
#     msg.attach(part)

#     # Send the email via Gmail's SMTP server
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())


# if __name__ == '__main__':
#     app.run(debug=True)

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


