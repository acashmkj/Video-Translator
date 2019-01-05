import boto3
import uuid
import requests

def createTranscribeJob(region, bucket, mediaFile):

	# Set up the Transcribe client 
	transcribe = boto3.client('transcribe')

	# Set up the full uri for the bucket and media file
	mediaUri = "https://" + "s3-" + region + ".amazonaws.com/" + bucket + '/' + mediaFile 

	print("\tCreating Job: " + "transcribe_" + mediaFile + " for " + mediaUri)

	# Use the uuid functionality to generate a unique job name.  Otherwise, the Transcribe service will return an error
	response = transcribe.start_transcription_job(TranscriptionJobName = "transcribe_" + uuid.uuid4().hex + "_" + mediaFile , \
		LanguageCode = "en-US", \
		MediaFormat = "mp4", \
		Media = { "MediaFileUri" : mediaUri } \
		# Settings = { "VocabularyName" : "MyVocabulary" } \
		)

	# return the response structure found in the Transcribe Documentation
	return response

def getTranscriptionJobStatus(jobName):
	transcribe = boto3.client('transcribe')

	response = transcribe.get_transcription_job(TranscriptionJobName=jobName)
	return response

def getTranscript(transcriptURI):
	# Get the resulting Transcription Job and store the JSON response in transcript
	result = requests.get(transcriptURI)

	return result.text
