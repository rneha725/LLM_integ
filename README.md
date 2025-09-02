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
