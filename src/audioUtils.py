
import boto3
import os
import json
import contextlib
from moviepy.editor import *
from moviepy import editor
from contextlib import closing

def writeAudio( output_file, stream ):

	bytes = stream.read()
	
	print "\t==> Writing ", len(bytes), "bytes to audio file: ", output_file
	try:
		# Open a file for writing the output as a binary stream
		with open(output_file, "wb") as file:
			file.write(bytes)
		
		if file.closed:
				print "\t==>", output_file, " is closed"
		else:
				print "\t==>", output_file, " is NOT closed"
	except IOError as error:
		# Could not write to file, exit gracefully
		print(error)
		sys.exit(-1)


def createAudioTrackFromTranslation( region, transcript, sourceLangCode, targetLangCode, audioFileName ):
	print( "\n==> createAudioTrackFromTranslation " )
	
	# Set up the polly and translate services
	client = boto3.client('polly')
	translate = boto3.client(service_name='translate', region_name=region, use_ssl=True)

	#get the transcript text
	temp = json.loads( transcript)
	transcript_txt = temp["results"]["transcripts"][0]["transcript"]
	
	voiceId = getVoiceId( targetLangCode )
	
	# Now translate it.
	translated_txt = unicode((translate.translate_text(Text=transcript_txt, SourceLanguageCode=sourceLangCode, TargetLanguageCode=targetLangCode))["TranslatedText"])[:2999]

	# Use the translated text to create the synthesized speech
	response = client.synthesize_speech( OutputFormat="mp3", SampleRate="22050", Text=translated_txt, VoiceId=voiceId)
	
	if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
		print( "\t==> Successfully called Polly for speech synthesis")
		writeAudioStream( response, audioFileName )
	else:
		print( "\t==> Error calling Polly for speech synthesis")

	
def writeAudioStream( response, audioFileName ):
	# Take the resulting stream and write it to an mp3 file
	if "AudioStream" in response:
		with closing(response["AudioStream"]) as stream:
			output = audioFileName
			writeAudio( output, stream )

def getVoiceId( targetLangCode ):

	# Feel free to add others as desired
	if targetLangCode == "es":
		voiceId = "Enrique"
	elif targetLangCode == "de":
		voiceId = "Hans"
	elif targetLangCode == "cmn":
		voiceId = "Zhiyu"
	elif targetLangCode == "da":
		voiceId = "Mads"
	elif targetLangCode == "nl":
		voiceId = "Ruben"
	elif targetLangCode == "fr":
		voiceId = "Mathieu"
	elif targetLangCode == "is":
		voiceId = "Karl"
	elif targetLangCode == "it":
		voiceId = "Giorgio"
	elif targetLangCode == "ja":
		voiceId = "Takumi"
	elif targetLangCode == "ko":
		voiceId = "Seoyeon"
	elif targetLangCode == "nb":
		voiceId = "Liv"
	elif targetLangCode == "pl":
		voiceId = "Jacek"
	elif targetLangCode == "pt":
		voiceId = "Ricardo"
	elif targetLangCode == "ro":
		voiceId = "Carmen"
	elif targetLangCode == "ru":
		voiceId = "Maxim"
	elif targetLangCode == "sv":
		voiceId = "Astrid"
	elif targetLangCode == "tr":
		voiceId = "Filiz"
	elif targetLangCode == "cy":
		voiceId = "Gwyneth"

	return voiceId
	
	
def getSecondsFromTranslation( textToSynthesize, targetLangCode, audioFileName ):

	# Set up the polly and translate services
	client = boto3.client('polly')
	translate = boto3.client(service_name='translate', region_name="us-east-1", use_ssl=True)

	# Use the translated text to create the synthesized speech
	response = client.synthesize_speech( OutputFormat="mp3", SampleRate="22050", Text=textToSynthesize, VoiceId=getVoiceId( targetLangCode ) )

	# write the stream out to disk so that we can load it into an AudioClip
	writeAudioStream( response, audioFileName )

	# Load the temporary audio clip into an AudioFileClip
	audio = AudioFileClip( audioFileName)

	# return the duration
	return audio.duration
