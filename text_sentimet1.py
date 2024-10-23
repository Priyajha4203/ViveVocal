import os

from collections import Counter

# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import azure.cognitiveservices.speech as speech_sdk
global speech_config

# Get Configuration Settings
ai_key = "b32f134094a2432fa1293380952bfa61"
ai_region = "eastus"
speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)


def speak_fun(texxt):
    speak = speech_synthesizer.speak_text_async(texxt).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
        
def seprate_method_analysis(text):
    #Loading Credentials    
    ai_endpoint = "https://lang097867575.cognitiveservices.azure.com/"
    ai_key = "d59c070ceefa417687e0b85ddf37a7c8"
    
    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    
    print("---:: Your text is processed , I am Telling about sentiment and other things in your given input ::---")
    speak_fun("Your text is processed")
    # Get language
    
    detectedLanguage = ai_client.detect_language(documents=[text])[0]
    print("Language :")
    print('{}'.format(detectedLanguage.primary_language.name))
    speak_fun(f"Language of your input is {detectedLanguage.primary_language.name}")
    print("--------------------------------------------------------------------")
    
    # Get sentiment
    sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
    print("Sentiment : ")
    print("{}".format(sentimentAnalysis.sentiment))
    
    speak_fun(f"Sentiment of your input is {sentimentAnalysis.sentiment}")
     
     
    # Get key phrases
    phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
    #count_kpharas=0
    print("--------------------------------------------------------------------")
    print("Giving Key phrases : ")
    speak_fun("Key phrases of this statement is ")
    if len(phrases) > 0:
        for phrase in phrases:
            print(phrase)
        for phrase in phrases[:5]:
            speak_fun(phrase)
    else:
        print("No Key Phrases present in this statement ")
        speak_fun("No Key Phrases present in this statement")
             
             
    # Get entities
    entities = ai_client.recognize_entities(documents=[text])[0].entities
    print("--------------------------------------------------------------------")

    # print(entities)
    if len(entities) > 0:
        print(f"Entities : ")
        speak_fun("Entities present in this statement")
        for entity in entities:
            print("Name :",entity.text," : Category : ",entity.category)
        for entit in entities:
            speak_fun(entity.text)
               
    else:
        print("No Entities present in this statement")
        speak_fun("No Entities present in this statement ")
        
    #Get links
    entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
    print("--------------------------------------------------------------------")

    if entities:
        print("Links : ")
        speak_fun("The fifth thing which is the Link of this statement")
            
       
        linked_name = []
        linked = []
        
        for linked_entity in entities[:5]:  #taki only the first 5 entities
            linked_name.append(linked_entity.name)
            linked.append(linked_entity.url)
        
        #create a table with entity names and links
        print({"Entity": linked_name, "Links": linked})
    else:
        print("No linked entities found.")
        speak_fun("No linked entities found.")



def text_analysis(flag=0,content=''):
    try:
        
        if flag==0:
            #analyze each text file in the reviews folder
            reviews_folder = 'speech_text'
            filelist=os.listdir(reviews_folder)
            #print(filelist)
            sorted_reviews = sorted(filelist, key=lambda x: int(x.split('_')[1].split('.')[0]))
            #print(sorted_reviews)
            file_name=sorted_reviews[-1]
            print(file_name)
            
            #print('\nNumber of Promot asked is : ' +f"{len(os.listdir(reviews_folder))}" ,divider=True)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print("Processing your Input")
            seprate_method_analysis(text)
   
   
    except Exception as ex:
        print(ex)