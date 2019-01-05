from moviepy.editor import *
from moviepy import editor
from moviepy.video.tools.subtitles import SubtitlesClip
#import moviepy.video.fx.all as vfx 
from time import gmtime, strftime


# Load the clips outputed from makevideo.bat
print strftime("%H:%M:%S", gmtime()), "Reading video English clip..."
english = VideoFileClip("subtitledVideo-en.mp4")
english = english.subclip( 0, 15).set_duration(15)

print strftime("%H:%M:%S", gmtime()), "Reading video Spanish clip..."
spanish = VideoFileClip("subtitledVideo-es.mp4")
spanish = spanish.subclip( 15, 30).set_duration(15)

print strftime("%H:%M:%S", gmtime()), "Reading video German clip..."
german = VideoFileClip("subtitledVideo-de.mp4")
german = german.subclip( 30, 45).set_duration(15)



print strftime("%H:%M:%S", gmtime()), "Creating title..."
# Generate a text clip. You can customize the font, color, etc.
toptitle = TextClip("Creating Subtitles and Translations Using Amazon Services:\n\nAmazon Transcribe\nAmazon Translate\nAmazon Polly",fontsize=36,color='white', bg_color='black', method="caption", align="center", size=english.size)
toptitle.set_duration(5)


subtitle1 = TextClip("re:Invent 2017 Keynote Address",fontsize=36,color='white', bg_color='black', method="caption", align="center", size=english.size)
subtitle1.set_duration(5)

subtitle2 = TextClip( "\nAndy Jassy, President and CEO of Amazon Web Services", fontsize=28, color='white', bg_color='black', method="caption", align="center ", size=english.size)
subtitle2.set_duration(5)

# Composite the video clips into a title page
title = CompositeVideoClip( [ toptitle, subtitle1.set_start(5), subtitle2.set_start(9)] ).set_duration(15)


#Create text clips for the various different translations
est = TextClip("English Subtitles\nUsing Amazon Transcribe",fontsize=24,color='white', bg_color='black', method="caption", align="center", size=english.size)
est = est.set_pos('center').set_duration(2.5)

sst = TextClip("Spanish Subtitles\nUsing Amazon Transcribe, Amazon Translate, and Amazon Polly",fontsize=24,color='white', bg_color='black', method="caption", align="center", size=english.size)
sst = sst.set_pos('center').set_duration(2.5)

dst = TextClip("German Subtitles\nUsing Amazon Transcribe, Amazon Translate, and Amazon Polly",fontsize=24,color='white', bg_color='black', method="caption", align="center", size=english.size)
dst = dst.set_pos('center').set_duration(2.5)

print strftime("%H:%M:%S", gmtime()), "Concatenating videos"

# concatenate the various titles, subtitles, and clips together
combined = concatenate_videoclips( [title.crossfadeout(2), est, english, sst, spanish, dst, german] )

# Write the result to a file (many options available !)
print strftime("%H:%M:%S", gmtime()), "Writing concatnated video"
combined.write_videofile("combined.mp4",  codec="libx264", audio_codec="aac", fps=24)
