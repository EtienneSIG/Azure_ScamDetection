# Azure_ScamDetection

## Summary

This script uses the Azure Cognitive Services Computer Vision API and OpenAI GPT-4 API to analyze and tell if the image is an scams. It extracts the text from the image (OCR), sends it to the GPT-4 model for translation and returns the result.

## Dependencies

- `azure.cognitiveservices.vision.computervision`
- `azure.cognitiveservices.vision.computervision.models`
- `msrest.authentication`
- `array`
- `os`
- `PIL`
- `sys`
- `time`
- `openai`
- `nltk`
- `json`

## Functions

### 1. `ComputerVision(endpoint, subscription_key, url_img)`

This function uses Azure's Computer Vision service to extract text from a given image URL. It authenticates with the service, sends a request to read the image, and waits for the result. Once the result is available, it prints the detected text line by line.

**Parameters:**

- `endpoint`: The endpoint of the Azure's Computer Vision service
- `subscription_key`: The subscription key for Azure's Computer Vision service
- `url_img`: The URL of the image to be analyzed

**Returns:**

- `prompt`: The text extracted from the image

### 2. `openaiTraduction(prompt, endpoint, key, model_id, api_version)`

This function uses OpenAI's GPT-3 model to translate the text extracted from the image. It initializes a client with the OpenAI service, sends a request for translation, and retrieves the result.

**Parameters:**

- `prompt`: The text to be translated
- `endpoint`: The endpoint of OpenAI's GPT-3 service
- `key`: The API key for OpenAI's GPT-3 service
- `model_id`: The ID of the GPT-3 model to be used
- `api_version`: The API version of OpenAI's GPT-3 service

**Returns:**

- `answer`: The translated text

### 3. `get_token_count(prompt)`

This function counts the number of tokens in a given text using the `nltk` library.

**Parameters:**

- `prompt`: The text to count the tokens for

**Returns:**

- The number of tokens in the text

## Main Execution

In the main execution, the script loads configuration details from a JSON file (API keys, endpoints, model ID, API version, etc.), performs text extraction from a given image URL using the `ComputerVision` function, and then sends the extracted text for translation using the `openaiTraduction` function. The result is then printed to the console.
