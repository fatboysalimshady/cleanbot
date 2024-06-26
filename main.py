
import time
import termux
import anthropic
import base64
import httpx
import os
from datetime import datetime
from pathlib import Path
import json
from PIL import Image, ImageOps
from anthropic.types import (
    ContentBlock,
    ContentBlockDeltaEvent,
    ContentBlockStartEvent,
    ContentBlockStopEvent,
    ImageBlockParam,
    Message,
    MessageDeltaEvent,
    MessageDeltaUsage,
    MessageParam,
    MessageStartEvent,
    MessageStopEvent,
    MessageStreamEvent,
    TextDelta,
    Usage,
)
from openai import OpenAI
OPEN_AI_KEY = os.environ.get("OPENAI_API_KEY")



# Get the current working directory
cwd = os.getcwd()
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)



base_filename = Path('photo.jpg')

def take_photo():
    new_filename = base_filename.with_name(f"{base_filename.stem}_{datetime.now().strftime('%Y%m%d%H%M')}{base_filename.suffix}")
    print(new_filename)
    # file_path = os.path.join(Path("/data/data/com.termux/files/home/storage/downloads/dev/deebotbase"), new_filename)
    filepath = f"/data/data/com.termux/files/home/storage/downloads/dev/deebotbase/images/{new_filename}"
    termux.Camera.takephoto(0,filepath)
    return filepath

def resize_photo(filepath):
    im = Image.open(filepath)
    im = ImageOps.exif_transpose(im)
    im.thumbnail((1000,1000))
    im = im.rotate(180)
    im.save(filepath)

def survey():
    x = 0
    while x < 5:
        take_action("rotate_right")
        time.sleep(0.5)
        new_filename = base_filename.with_name(f"{base_filename.stem}_{datetime.now().strftime('%Y%m%d%H%M')}_{x}{base_filename.suffix}")
        print(new_filename)
        # file_path = os.path.join(Path("/data/data/com.termux/files/home/storage/downloads/dev/deebotbase"), new_filename)
        filepath = f"/data/data/com.termux/files/home/storage/downloads/dev/deebotbase/images/{new_filename}"
        termux.Camera.takephoto(0,filepath)
        x = x + 1
    x = x + 1
    take_action("rotate_right")
    new_filename = base_filename.with_name(f"{base_filename.stem}_{datetime.now().strftime('%Y%m%d%H%M')}_{x}{base_filename.suffix}")
    print(new_filename)
    # file_path = os.path.join(Path("/data/data/com.termux/files/home/storage/downloads/dev/deebotbase"), new_filename)
    filepath = f"/data/data/com.termux/files/home/storage/downloads/dev/deebotbase/images/{new_filename}"
    termux.Camera.takephoto(0,filepath)
    return filepath  

#survey()

#ANTHROPIC

# messages = []

# x = 0
# while x < 10:
#     filepath = take_photo()
#     resize_photo(filepath)

#     with open(filepath, "rb") as image_file:
#         encoded_bytes = base64.b64encode(image_file.read())
#         encoded_string = encoded_bytes.decode('utf-8')


#     new_message={
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image",
#                         "source": {
#                             "type": "base64",
#                             "media_type": "image/jpeg",
#                             "data": encoded_string
#                         }
#                     },
#                     {
#                         "type": "text",
#                         "text": "remember, only respond with strictly json"
#                     }
#                 ]
#             }

#     messages.append(new_message) 
#     print(messages)
#     message = client.messages.create(
#         #model="claude-3-opus-20240229",
#         model = "claude-3-sonnet-20240229"
#         max_tokens=1000,
#         temperature=0,
#         system="""You are the navigation system of a simple robot, your job is to navigate an unknown indoor space given only images. 
#         the goal is to find a dog while avoiding bumping into any obsticles and exploring the whole environment. 
#         your response should include, what you see, what your planned next steps are and a next action along with the number of times that action takes place. only respond strictly in the following json schema:
#         {
#         "type": "object",
#         "properties": {
#             "what_do_you_see": {
#             "type": "string"
#             },
#             "planned_next_steps": {
#             "type": "string"
#             },
#             "action": {
#             "type": "string",
#             "enum": ["forward", "backward", "rotate_left", "rotate_right", "dog_found"]
#             },
#             "action_count_number": {
#             "type": "integer"
#             }
#         },
#         "required": ["what_do_you_see", "planned_next_steps", "action", "action_count_number"]
#         }
#         """
#         messages=messages
#     )

#     ai_response =   {
#                         "role": message.role,
#                         "content": message.content,
#                     }

#     messages.append(ai_response)


#     print(message.content[0].text)
#     take_action(message.content[0].text)


client = OpenAI()


messages = [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": """You are the navigation system of a simple robot, your job is to navigate an unknown indoor space given only images. 
        the goal is to find a dog while avoiding bumping into any obsticles and exploring the whole environment. 
        your response should include, what you see, what your planned next steps are and a next action along with the number of times that action takes place. only respond strictly in the following json schema:
        {
        "type": "object",
        "properties": {
            "what_do_you_see": {
            "type": "string"
            },
            "planned_next_steps": {
            "type": "string"
            },
            "action": {
            "type": "string",
            "enum": ["forward", "backward", "rotate_left", "rotate_right", "dog_found"]
            },
            "action_count_number": {
            "type": "integer"
            }
        },
        "required": ["what_do_you_see", "planned_next_steps", "action", "action_count_number"]
        }
        """
        }
      ]
    }
    ]

x = 0
while x < 2:
    filepath = take_photo()
    resize_photo(filepath)

    with open(filepath, "rb") as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
        encoded_string = encoded_bytes.decode('utf-8')


    new_message={
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encoded_string}"
          }
        },
        {
          "type": "text",
          "text": "remember, only respond with strictly json"
        }
      ]
    }

    messages.append(new_message) 
    message = client.chat.completions.create(
        model="gpt-4o",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages=messages
    )

    ai_response ={
                "role": "assistant",
                "content": [
                    {
                    "type": "text",
                    "text": f"{message.choices[0].message.content}"
                    }
                ]
                },

    messages.append(ai_response)


    print(message.choices[0].message.content)
    take_action(message.choices[0].message.content)
    