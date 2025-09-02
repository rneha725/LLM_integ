## Overview
This repo has some practice code I built using this course: https://learn.deeplearning.ai/courses/chatgpt-building-system

It integrates with open ai for instruction tuned LLM responses as well as for moderation responses. 
Each file covers a useful concept and `user_query.py` covers the user interaction of the system/model with the user. 

## Some pointers in instruction based LLMs:
- LLM is supervisly learnt model, which helps us predict the next word. For example, when asked, `What is the capital of France?` it can output anything, based on the data it used to train itself.
- Here we are looking at instruction tuned LLMs, e.g., chatgpt. We train in small sample using the instructions. To train better we get user feedback-> RHF Reinforced Human Feedback.
- Token: an LLM api is priced on the basis of tokens(input+output).
- We have three main components when we interact with the LLM model of openai: System <-> LLM Assistant <-> User
- System: Sets the tone, scope, behaviour of the responses.
- LLM Assistant: the one that generates user response by predicting the next word.
- User: creates inputs and prompts.
- Prompt based AI: we define the prompt for the system and interact accordingly.
- Moderation: 1. We have openai' moderation api. 2. We need to be resilient against prompt injections/manipulations. 3. We need to hide reasoning steps from the user.
- Prompt engineering involves creating cost effective and resileint prompts. Testing them and correct them continuously. 

## [general_ai_use.py](https://github.com/rneha725/LLM_integ/blob/main/general_ai_use.py)
While other functions are self explanatory, I will be focussing on the method: `get_completion_from_messages`. This will be used throughout the other files. To send the user input to the system/LLM
we used `openai.ChatCompletion.create` API. We need to provide the message which is an array. Each object in the array contains two keys: 1. role, 2. content. Role defines which component we want the content to apply to. For example, we can define the role as 'PJ master' and now out system will only give us PJs. For providing the user input we use role: 'user'. Example:

```js
messages =  [  
    {'role':'system', 'content':"""act like someone who only asks questions"""},    
    {'role':'user', 'content':"""write me an essay on parrots"""},  
]
```

This is the most basic usage, you can play with the arguments of this api, example, temperature, model name, max token usage, see: https://platform.openai.com/docs/guides/text

## [moderation_validate_output.py](https://github.com/rneha725/LLM_integ/blob/main/moderation_validate_output.py)
see: https://platform.openai.com/docs/guides/moderation

Provides moderation output as per the open ai policies, check the above link. It can give the input ratings in few categories defined in the policy, according to your model's need you can override the threshold.
We used api: `openai.Moderation.create` for this.

## [chain_instructions.py](https://github.com/rneha725/LLM_integ/blob/main/chain_instructions.py)
Here for the system message we have used a series of steps to get the response, go through and look at the system message, after that we have used `get_completion_from_messages` from the above file.

## [chain_prompts.py](https://github.com/rneha725/LLM_integ/blob/main/chain_prompts.py)
Prompt chaining is a useful concept when we want to build a system out of LLM model. It breaks down complex tasks in the prompts and the set of prompts can be seen as a state machine, the output of one prompt can be given to other to process. This is very similar to creating modules, we get effiecient usage of tokes, simplicity, more testability, easy integration with external tools, easy modifications etc.

## [prompt injection example](https://github.com/rneha725/LLM_integ/blob/main/customer_service.py) , [prompt_injection.py](https://github.com/rneha725/LLM_integ/blob/main/prompt_injection.py)
We can simply add in the system message to make the system resilent from prompt injections/manipulations.

## [user_query.py](https://github.com/rneha725/LLM_integ/blob/main/user_query.py)
`process_user_message` convers the main steps we use to process user query
- Context: we track all the messages user has sent in one chat
- moderation api: used for user input and LLM output
- chain of prompts, we have used two prompts, first one provides input to the other.

