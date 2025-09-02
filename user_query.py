import openai
import utils
from general_ai_use import get_completion_from_messages

'''
Note: we are going to use the function defined elsewhere to process user inputs, we will be chaining the prompts.
'''

delimiter = "####"
def __moderation_check(input) -> bool:
    response = openai.Moderation.create(input=input)
    moderation_output = response["results"][0]

    if moderation_output["flagged"]:
        return False
    
    return True
    
    
def process_user_message(user_input, all_messages=[]):
    if __moderation_check(user_input) == False:
        return "Sorry, we cannot process this user input."
    
    print("Step 1: Input passed moderation check.")
    
    category_and_product_response = utils.find_category_and_product_only(user_input)
    category_and_product_list = utils.read_string_to_list(category_and_product_response)

    print("Step 2: Extracted list of products.")

    product_information = utils.generate_output_string(category_and_product_list)
    
    print("Step 3: Looked up product information.")

    system_message = f"""
    You are a customer service assistant for a large electronic store. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask the user relevant follow-up questions.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        {'role': 'assistant', 'content': f"Relevant product information:\n{product_information}"}
    ]
    final_response = get_completion_from_messages(all_messages + messages)
    
    print("Step 4: Generated response to user question.")
    all_messages = all_messages + messages[1:]

    if __moderation_check(user_input) == False:
        return "Sorry, we cannot provide this information."
    
    print("Step 5: Response passed moderation check.")
    
    user_message = f"""
    Customer message: {delimiter}{user_input}{delimiter}
    Agent response: {delimiter}{final_response}{delimiter}

    Does the response sufficiently answer the question?
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    evaluation_response = get_completion_from_messages(messages)
    
    print("Step 6: Model evaluated the response.")

    
    if "Y" in evaluation_response:
        print("Step 7: Model approved the response.")
        return final_response, all_messages
    else:
        print("Step 7: Model disapproved the response.")
        neg_str = "I'm unable to provide the information you're looking for. I'll connect you with a human representative for further assistance."
        return neg_str, all_messages

user_input = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"
response,_ = process_user_message(user_input,[])
print(response)

def collect_messages(user_input):
    print(f"User Input = {user_input}")
    if user_input == "":
        return
    global context
    response, context = process_user_message(user_input, context)
    context.append({'role':'assistant', 'content':f"{response}"})
    

context = [ {'role':'system', 'content':"You are Service Assistant"} ]