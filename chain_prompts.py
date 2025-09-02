'''
Similar to chaining instructions but instead of doing everything in one prompt, focus on one component of the problem in one prompt and divide the problem
related to each compenent in one prompt and chain them. Similar to spaghetti code and modular code.
You can also react to different outputs of the prompts differently, something similar to state machines.

Modules has a lot of pros:
- easy testing
- tracking the state of the problem external to LLM
- easily modifiable
- you can use the external tools more easily
- reduces tokens in a prompt -> lower cost, low tokens in each prompt
'''
import json 
from general_ai_use import get_completion_from_messages
from utils import read_string_to_list, generate_output_string

#==================================== Prompt 1 =====================================================================================================
delimiter = "####"
system_message_for_category_product_object = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Output a python list of objects, where each object has \
the following format:
    'category': <one of Computers and Laptops, \
    Smartphones and Accessories, \
    Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, 
    Audio Equipment, Cameras and Camcorders>,
OR
    'products': <a list of products that must \
    be found in the allowed products below>

Where the categories and products must be found in \
the customer service query.
If a product is mentioned, it must be associated with \
the correct category in the allowed products list below.
If no products or categories are found, output an \
empty list.

Allowed products: 

Computers and Laptops category:
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Cameras and Camcorders category:
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera

Only output the list of objects, with nothing else.
"""
user_message_1 = f"""
    tell me about the smartx pro phone and the fotosnap camera, the dslr one.
"""
messages =  [  
    {'role':'system', 'content': f"{system_message_for_category_product_object}"},    
    {'role':'user', 'content': f"{delimiter}{user_message_1}{delimiter}"},  
]

# product information
products = {
    "TechPro Ultrabook": {
        "name": "TechPro Ultrabook",
        "category": "Computers and Laptops",
        "brand": "TechPro",
        "model_number": "TP-UB100",
        "warranty": "1 year",
        "rating": 4.5,
        "features": ["13.3-inch display", "8GB RAM", "256GB SSD", "Intel Core i5 processor"],
        "description": "A sleek and lightweight ultrabook for everyday use.",
        "price": 799.99
    },
    "BlueWave Gaming Laptop": {
        "name": "BlueWave Gaming Laptop",
        "category": "Computers and Laptops",
        "brand": "BlueWave",
        "model_number": "BW-GL200",
        "warranty": "2 years",
        "rating": 4.7,
        "features": ["15.6-inch display", "16GB RAM", "512GB SSD", "NVIDIA GeForce RTX 3060"],
        "description": "A high-performance gaming laptop for an immersive experience.",
        "price": 1199.99
    },
    "FotoSnap Instant Camera": {
        "name": "FotoSnap Instant Camera",
        "category": "Cameras and Camcorders",
        "brand": "FotoSnap",
        "model_number": "FS-IC10",
        "warranty": "1 year",
        "rating": 4.1,
        "features": ["Instant prints", "Built-in flash", "Selfie mirror", "Battery-powered"],
        "description": "Create instant memories with this fun and portable instant camera.",
        "price": 69.99
    }
}

user_message_1 = """
    tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also tell me about your tvs
"""

category_and_product_response_1 = """
    [
        {'category': 'Smartphones and Accessories'},
        {'category': 'Cameras and Camcorders'}
    ]
"""

category_and_product_list = read_string_to_list(category_and_product_response_1)
print(category_and_product_list)
'''
Output:
    [{'category': 'Smartphones and Accessories'}, {'category': 'Cameras and Camcorders'}]
'''

product_information_for_user_message_1 = generate_output_string(category_and_product_list)
print(product_information_for_user_message_1)
'''
Output:
    {
        "name": "FotoSnap Instant Camera",
        "category": "Cameras and Camcorders",
        "brand": "FotoSnap",
        "model_number": "FS-IC10",
        "warranty": "1 year",
        "rating": 4.1,
        "features": [
            "Instant prints",
            "Built-in flash",
            "Selfie mirror",
            "Battery-powered"
        ],
        "description": "Create instant memories with this fun and portable instant camera.",
        "price": 69.99
    }
'''

#==================================== Prompt 2 using the formatted output of the prompt 1 ======================================================
system_message = f"""
    You are a customer service assistant for a large electronic store. Respond in a friendly and helpful tone, with very concise answers. 
    Make sure to ask the user relevant follow up questions.
"""
user_message_1 = f"""
    tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also tell me about your tvs
"""
messages =  [  
    {'role':'system', 'content': system_message},   
    {'role':'user', 'content': user_message_1},  
    {'role':'assistant', 'content': f"""Relevant product information: {product_information_for_user_message_1}"""},   
]
final_response = get_completion_from_messages(messages)
print(final_response)
'''
Output:
    The FotoSnap Instant Camera (model FS-IC10) is a portable instant camera that allows you to create instant prints with features like a built-in flash 
    and selfie mirror. It comes with a 1-year warranty and is priced at $69.99. Is there anything specific you would like to know about the FotoSnap camera
    or any other product?
'''


''''
Note: 
- more focused prompts
- context limitations for LLMs, loading the prod info in the prompt can cost us tokens
'''