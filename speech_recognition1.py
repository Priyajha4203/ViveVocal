from datetime import datetime
import os
from text_sentimet1 import text_analysis ,speak_fun
import azure.cognitiveservices.speech as speech_sdk
from playsound import playsound


def main():
    try:
        global command1
        global speech_config

        # Get Configuration Settings
        ai_key = "b32f134094a2432fa1293380952bfa61"
        ai_region = "eastus"

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
        print(f'Ready to use speech service in: {speech_config.region}')
       
        command1 = TranscribeCommand()
            
        drictory="speech_text"
        #maintatinig the file count in directory 
        fileslist=os.listdir("speech_text")
        lenfl=len(fileslist)
        
        if command1 != '':
            with open(f"speech_text/review_{lenfl+1}.txt","x") as f:
                f.write(f"{command1}") 
                print(f"Your speaked text is saved in File name : {f"reveiw_{lenfl+1}.txt"}")
                f.close()     
            text_analysis()
        else:
            print("I can't hear any specific command kindly speak Again") 
            speak_fun("I can't hear any specific command kindly speak Again" )

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''


    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')


    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
          
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command



if __name__ == "__main__":
    main()

