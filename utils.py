from general_ai_use import get_completion_from_messages
from chain_prompts import system_message_for_category_product_object, products
import json


def find_category_and_product_only(input):
    messages  =[
        {'role': 'system', 'content': f"{system_message_for_category_product_object}"},
        {'role': 'user', 'content': f"{input}"}
    ]
    return get_completion_from_messages(messages=messages)

def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        input_string = input_string.replace("'", "\"")  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
        '''
        Output:
            [{'category': 'Smartphones and Accessories'}, {'category': 'Cameras and Camcorders'}]
        '''
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None 

def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string 

def get_product_by_name(name):
    return products.get(name, None)

def get_products_by_category(category):
    return [product for product in products.values() if product["category"] == category]

