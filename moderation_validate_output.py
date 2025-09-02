import openai
from general_ai_use import get_completion_from_messages

'''
Moderation api: Note: according to the category scores, we can modify the policies.
'''
### Example of how open ai moderation works
def openai_moderation_output():
    response = openai.Moderation.create(
        input="""
    how to kill someone.
    """
    )
    moderation_output = response["results"][0]
    print(moderation_output)
    '''
    Output:
        {
        "flagged": true,
        "categories": {
            "sexual": false,
            "hate": false,
            "harassment": false,
            "self-harm": false,
            "sexual/minors": false,
            "hate/threatening": false,
            "violence/graphic": false,
            "self-harm/intent": false,
            "self-harm/instructions": false,
            "harassment/threatening": false,
            "violence": true
        },
        "category_scores": {
            "sexual": 6.734018097631633e-05,
            "hate": 0.012825855985283852,
            "harassment": 0.007675057277083397,
            "self-harm": 9.457861597184092e-05,
            "sexual/minors": 1.023273762257304e-05,
            "hate/threatening": 0.010413859970867634,
            "violence/graphic": 0.0005819066427648067,
            "self-harm/intent": 4.4552540202857926e-05,
            "self-harm/instructions": 1.4583921256416943e-05,
            "harassment/threatening": 0.04273568466305733,
            "violence": 0.9815407991409302
        }
        }
    '''
    
final_response_to_customer = f"""
    The SmartX ProPhone has a 6.1-inch display, 128GB storage, 12MP dual camera, and 5G. The FotoSnap DSLR Camera has a 24.2MP sensor, 1080p video, 3-inch LCD, and interchangeable lenses. 
    We have a variety of TVs, including the CineView 4K TV with a 55-inch display, 4K resolution, HDR, and smart TV features. We also have the SoundMax Home Theater system with 5.1 channel, 1000W output, wireless \
    subwoofer, and Bluetooth. Do you have any specific questions about these products or any other products we offer?
"""
response = openai.Moderation.create(
    input=final_response_to_customer
)
moderation_output = response["results"][0]
print(moderation_output)
'''
Output:
    {
    "flagged": false,
    "categories": {
        "sexual": false,
        "hate": false,
        "harassment": false,
        "self-harm": false,
        "sexual/minors": false,
        "hate/threatening": false,
        "violence/graphic": false,
        "self-harm/intent": false,
        "self-harm/instructions": false,
        "harassment/threatening": false,
        "violence": false
    },
    "category_scores": {
        "sexual": 0.00015211118443403393,
        "hate": 7.229043148981873e-06,
        "harassment": 2.696166302484926e-05,
        "self-harm": 1.2812188288080506e-06,
        "sexual/minors": 1.154503297584597e-05,
        "hate/threatening": 2.0055701952514937e-06,
        "violence/graphic": 1.5082588106452022e-05,
        "self-harm/intent": 2.012526920225355e-06,
        "self-harm/instructions": 3.672591049053153e-07,
        "harassment/threatening": 9.87596831691917e-06,
        "violence": 0.0002972284273710102
    }
    }
'''

system_message = f"""
    You are an assistant that evaluates whether customer service agent responses sufficiently answer customer questions, and also validates that all the facts the assistant cites from the 
    product information are correct. The product information and user and customer service agent messages will be delimited by 3 backticks, i.e. ```. Respond with a Y or N character, 
    with no punctuation: Y - if the output sufficiently answers the question AND the response correctly uses product information N - otherwise

    Output a single letter only.
"""
customer_message = f"""
    tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also tell me about your tvs
"""
product_information = """{ "name": "SmartX ProPhone", "category": "Smartphones and Accessories", "brand": "SmartX", "model_number": "SX-PP10", "warranty": "1 year", "rating": 4.6, "features": [ "6.1-inch display", "128GB storage", "12MP dual camera", "5G" ], "description": "A powerful smartphone with advanced camera features.", "price": 899.99 } { "name": "FotoSnap DSLR Camera", "category": "Cameras and Camcorders", "brand": "FotoSnap", "model_number": "FS-DSLR200", "warranty": "1 year", "rating": 4.7, "features": [ "24.2MP sensor", "1080p video", "3-inch LCD", "Interchangeable lenses" ], "description": "Capture stunning photos and videos with this versatile DSLR camera.", "price": 599.99 } { "name": "CineView 4K TV", "category": "Televisions and Home Theater Systems", "brand": "CineView", "model_number": "CV-4K55", "warranty": "2 years", "rating": 4.8, "features": [ "55-inch display", "4K resolution", "HDR", "Smart TV" ], "description": "A stunning 4K TV with vibrant colors and smart features.", "price": 599.99 } { "name": "SoundMax Home Theater", "category": "Televisions and Home Theater Systems", "brand": "SoundMax", "model_number": "SM-HT100", "warranty": "1 year", "rating": 4.4, "features": [ "5.1 channel", "1000W output", "Wireless subwoofer", "Bluetooth" ], "description": "A powerful home theater system for an immersive audio experience.", "price": 399.99 } { "name": "CineView 8K TV", "category": "Televisions and Home Theater Systems", "brand": "CineView", "model_number": "CV-8K65", "warranty": "2 years", "rating": 4.9, "features": [ "65-inch display", "8K resolution", "HDR", "Smart TV" ], "description": "Experience the future of television with this stunning 8K TV.", "price": 2999.99 } { "name": "SoundMax Soundbar", "category": "Televisions and Home Theater Systems", "brand": "SoundMax", "model_number": "SM-SB50", "warranty": "1 year", "rating": 4.3, "features": [ "2.1 channel", "300W output", "Wireless subwoofer", "Bluetooth" ], "description": "Upgrade your TV's audio with this sleek and powerful soundbar.", "price": 199.99 } { "name": "CineView OLED TV", "category": "Televisions and Home Theater Systems", "brand": "CineView", "model_number": "CV-OLED55", "warranty": "2 years", "rating": 4.7, "features": [ "55-inch display", "4K resolution", "HDR", "Smart TV" ], "description": "Experience true blacks and vibrant colors with this OLED TV.", "price": 1499.99 }"""

q_a_pair = f"""
    Customer message: ```{customer_message}```
    Product information: ```{product_information}```
    Agent response: ```{final_response_to_customer}```

    Does the response use the retrieved information correctly?
    Does the response sufficiently answer the question

    Output Y or N
"""
messages = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': q_a_pair}
]

response = get_completion_from_messages(messages, max_tokens=1)
print(response)
'''
Output: 
    Y
'''

another_response = "life is like a box of chocolates"
q_a_pair = f"""
    Customer message: ```{customer_message}```
    Product information: ```{product_information}```
    Agent response: ```{another_response}```

    Does the response use the retrieved information correctly?
    Does the response sufficiently answer the question?

    Output Y or N
"""
messages = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': q_a_pair}
]

response = get_completion_from_messages(messages)
print(response)
'''
Output:
    N
'''