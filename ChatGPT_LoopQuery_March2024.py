# -*- coding: utf-8 -*-
"""
Created on Friday March 22 11:24:40 2024
@author: chris.pham
"""

# The following code will work for Python 3.7.x+

# ----------------------------------------------
# REMEMBER TO RUN THESE PIP COMMANDS if you have an older OpenAI:
# pip uninstall openai
# Note: the command may look like this in your venv  C:\Python310\Scripts\pip install openai pandas python-dotenv

# ----------------------------------------------
# RUN THESE COMMANDS FROM THE TERMINAL
# Create the virtual environment called "venv"
# python -m venv venv   

# from venv
# pip install openai==0.28 pandas python-dotenv

# Activate the venv 
# Windows command:
# venv\Scripts\activate
# MacOS or Linux command: 
# source chatgpt_env/bin/activate

import os
import openai  # remember to pip install pandas openai
from dotenv import load_dotenv  # remember to pip install python-dotenv


# Set the API key
"""
# Visit your API Keys page to retrieve the API key you'll use in your requests.
# Remember that your API key is a secret! Do not share it with others or expose 
# it in any client-side code (browsers, apps).
https://platform.openai.com/account/api-keys 
"""
load_dotenv("env_example")
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Prompt the user to select a model. Reference for models: https://platform.openai.com/docs/models
print("Refer to https://platform.openai.com/docs/models for available model options.")
model = input("\nEnter the model you want to use (e.g., 'gpt-3.5-turbo', 'gpt-4'): ")

# Prompt the user to set temperature
print("\nTemperature controls the randomness of responses.")
print("Range: 0 to 1 (0 is more deterministic, 1 is more random)")
try:
    temperature = float(input("Enter a temperature value (default 0.7): "))
except ValueError:
    temperature = 0.7
    print("Invalid input. Using default temperature of 0.7")

# Prompt the user to set max tokens
print("\nMax Tokens: Sets the maximum length for the model’s output.")
try:
    max_tokens = int(input("Enter the max tokens value (e.g., 50, 100, 300; default 150): "))
except ValueError:
    max_tokens = 150
    print("Invalid input. Using default max tokens of 150")

# Prompt the user to set top_p
print("\nTop P (Nucleus Sampling): Controls response variety by only considering the top 'P' percent of probable words.")
print("Range: 0 to 1 (0.1 considers fewer words, 1 considers all probable words)")
try:
    top_p = float(input("Enter a top_p value (default 1.0): "))
except ValueError:
    top_p = 1.0
    print("Invalid input. Using default top_p of 1.0")

# Prompt the user to set frequency penalty
print("\nFrequency Penalty: Reduces repetition by decreasing the likelihood of frequently used words.")
print("Range: 0 to 2 (higher values reduce repetition more)")
try:
    frequency_penalty = float(input("Enter a frequency penalty value (default 0): "))
except ValueError:
    frequency_penalty = 0
    print("Invalid input. Using default frequency penalty of 0")

# Prompt the user to set presence penalty
print("\nPresence Penalty: Promotes the introduction of new topics in the conversation.")
print("Range: 0 to 2 (higher values encourage introducing new topics)")
try:
    presence_penalty = float(input("Enter a presence penalty value (default 0): "))
except ValueError:
    presence_penalty = 0
    print("Invalid input. Using default presence penalty of 0")

while True:
    myrole = input("\nWhat is my role? (or type 'quitme' to quit): \n")
    if myrole == 'quitme':
        break
    mytask = input("\nWhat is my task? (or type 'quitme' to quit): \n")
    if mytask == 'quitme':
        break

    messages = [{"role": "system", "content": myrole}]
    messages.append({"role": "user", "content": mytask})

    # Use selected model, temperature, max_tokens, top_p, frequency_penalty, and presence_penalty in the API call
    answers = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages
    )

    print("----------------\n")
    print(answers['choices'][0]['message']['content'])
    print("----------------\n")
