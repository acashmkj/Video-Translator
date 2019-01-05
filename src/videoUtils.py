from moviepy.editor import *
from moviepy import editor
from moviepy.video.tools.subtitles import SubtitlesClip
from time import gmtime, strftime
from audioUtils import *

def annotate(clip, txt, txt_color='white', fontsize=24, font='Arial-Bold'):
    # Writes a text at the bottom of the clip  'Xolonium-Bold'
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=font, color=txt_color).on_color(color=[0,0,0])
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 50))])
    return cvc.set_duration(clip.duration)
	
def createVideo( originalClipName, subtitlesFileName, outputFileName, alternateAudioFileName, useOriginalAudio=True ):
	# This function is used to put all of the pieces together.   
	# Note that if we need to use an alternate audio track, the last parm should = False
	
	print( "\n==> createVideo " )

	# Load the original clip
	print "\t" + strftime("%H:%M:%S", gmtime()), "Reading video clip: " + originalClipName 
	clip = VideoFileClip(originalClipName)
	print "\t\t==> Original clip duration: " + str(clip.duration)

	if useOriginalAudio == False:
		print strftime( "\t" + "%H:%M:%S", gmtime()), "Reading alternate audio track: " + alternateAudioFileName
		audio = AudioFileClip(alternateAudioFileName)
		audio = audio.subclip( 0, clip.duration )
		audio.set_duration(clip.duration)
		print "\t\t==> Audio duration: " + str(audio.duration)
		clip = clip.set_audio( audio )
	else:
		print strftime( "\t" + "%H:%M:%S", gmtime()), "Using original audio track..."
		
	# Create a lambda function that will be used to generate the subtitles for each sequence in the SRT
	generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=24, color='white')

	# read in the subtitles files
	print "\t" + strftime("%H:%M:%S", gmtime()), "Reading subtitle file: " + subtitlesFileName 
	subs = SubtitlesClip(subtitlesFileName, generator)
	print "\t\t==> Subtitles duration before: " + str(subs.duration)
	subs = subs.subclip( 0, clip.duration - .001)
	subs.set_duration( clip.duration - .001 )
	print "\t\t==> Subtitles duration after: " + str(subs.duration)
	print "\t" + strftime("%H:%M:%S", gmtime()), "Reading subtitle file complete: " + subtitlesFileName 


	print "\t" + strftime( "%H:%M:%S", gmtime()), "Creating Subtitles Track..."
	annotated_clips = [annotate(clip.subclip(from_t, to_t), txt) for (from_t, to_t), txt in subs]



	print "\t" + strftime( "%H:%M:%S", gmtime()), "Creating composited video: " + outputFileName
	# Overlay the text clip on the first video clip
	final = concatenate_videoclips( annotated_clips )

	print "\t" + strftime( "%H:%M:%S", gmtime()), "Writing video file: " + outputFileName 
	final.write_videofile(outputFileName)
