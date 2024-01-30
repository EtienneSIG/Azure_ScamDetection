from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import openai
import nltk
import json 
import argparse

nltk.download('punkt')
'''
Authenticate
Authenticates your credentials and creates a client.
'''

# Load config values
with open(r'config.json') as config_file:
    config_details = json.load(config_file)
    print(config_details)

# Setting up the model detail
gpt_key = config_details['OPENAI_API_KEY']
gpt_endpoint = config_details['OPENAI_API_BASE']
gpt_token_max = config_details['OPENAI_NB_TOKENS']
gpt_model_id=config_details['COMPLETIONS_MODEL']
gpt_api_version=config_details['OPENAI_API_VERSION'] 

computerVision_key=config_details['COMPUTER_VISION_KEY']
computerVision_endpoint=config_details['COMPUTER_VISION_ENDPOINT'] 





def ComputerVision(endpoint,subscription_key,url_img):
    prompt=""
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    '''
    END - Authenticate
    '''

    '''
    OCR: Read File using the Read API, extract text - remote
    This example will extract text in an image, then print results, line by line.
    This API call can also extract handwriting style text (not shown).
    '''
 
    # Get an image with text
    # read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"
    read_image_url = url_img
    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(read_image_url,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
    time.sleep(1)

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                #print(line.text)
                prompt = prompt +"\n"+ line.text
            #print(line.bounding_box)
    print()
    '''
    END - Read File - remote
    '''
    return prompt

def openaiTraduction(prompt,endpoint,key,model_id,api_version):

    client= openai.AzureOpenAI(
        azure_endpoint = endpoint,
        api_version=api_version,
        api_key = key
    )

    prompt=[{"role": "user", "content": prompt }]
    completion = client.chat.completions.create(model=model_id,
                                                  messages=prompt,
                                                  #max_tokens=get_token_count(prompt)*2 +96,
                                                  max_tokens=20000,
                                                  # stop=".",
                                                  temperature=0.7,
                                                  n=1,
                                                  top_p=0.95,
                                                  frequency_penalty=0,
                                                  presence_penalty=0,
                                                  stop=None
                                                  )

    answer = f"{completion.choices[0].message.content}"
    return answer

################################################################
##Get the number of token from a prompt
################################################################
def get_token_count(prompt):
    return len(nltk.word_tokenize(prompt))

if __name__ == "__main__":
        #Command line
    # Initialize parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help = "python scamDetection.py -i <image or image url> \n example python scamDetection.py -i \"https://cdnx.nextinpact.com/data-next/image/bd/171324.jpeg\" ", required=True)
    
    #Read argument
    args = parser.parse_args()
    
    url_img= args.image
    #url_img = "https://cdnx.nextinpact.com/data-next/image/bd/171324.jpeg"
    
    prompt=""
    answer=""
    message=""

    message=ComputerVision(computerVision_endpoint,computerVision_key,url_img)
    print(message)

    prompt = "Explain whether the following message is a scam or not : " + message 

    #answer=openaiTraduction(env_var.openai_endpoint,env_var.openai_key,prompt)
    answer=openaiTraduction(prompt,gpt_endpoint,gpt_key,gpt_model_id,gpt_api_version)

    print(answer)