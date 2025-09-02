import os
import openai
import tiktoken
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.OpenAI()
openai.api_key  = os.environ['OPENAI_API_KEY']

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
    )
    return response.choices[0].message["content"]

def get_completion_and_token_count(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    content = response.choices[0].message["content"]
    
    token_dict = {
        'prompt_tokens':response['usage']['prompt_tokens'],
        'completion_tokens':response['usage']['completion_tokens'],
        'total_tokens':response['usage']['total_tokens'],
    }
    return content, token_dict

####=========================== Function usages ===========================####
response = get_completion("What is the capital of France?")
print(response) 
'''
Output:
    The capital of France is Paris.
'''

'''
Note:
    system <-> LLM assistant <-> User
    Setting the system message is basically setting the chatgpt prompt and after that all the user query will be answered as they are interacting with the system.
'''
messages =  [  
    {'role':'system', 'content':"""act like someone who only asks questions"""},    
    {'role':'user', 'content':"""write me an essay on parrots"""},  
] 
response = get_completion_from_messages(messages, temperature=1)
print(response)
'''
Output:
    What makes parrots special among all bird species? How do parrots communicate with each other and their human companions? 
    What are the different types and species of parrots found around the world? ...
'''
messages = [
    {'role':'system', 'content':"""You are an assistant who responds in the style of Dr Seuss."""},    
    {'role':'user', 'content':"""write me a very short poem about a happy carrot"""},  
] 

response, token_dict = get_completion_and_token_count(messages)
print(token_dict) 
'''
Output:
    {'prompt_tokens': 37, 'completion_tokens': 89, 'total_tokens': 126}
'''
