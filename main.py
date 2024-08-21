
import time
import termux
import base64
import httpx
import os
from datetime import datetime
from pathlib import Path
import json
from PIL import Image, ImageOps
import requests
from openai import OpenAI

# from elevenlabs.client import ElevenLabs
# from elevenlabs import save
import termux

# elclient = ElevenLabs(
#   api_key="" # Defaults to ELEVEN_API_KEY
# )

# def TTS(text):
#   audio = elclient.generate(
#     text=text,
#     voice="Rachel",
#     model="eleven_multilingual_v2"
#   )
#   save(audio, "my-file.mp3")
#   termux.Media.play("my-file.mp3")
def TTS(text):
  termux.TTS.tts_speak(text=text, rate=2)

    #   Parameters
    # ----------
    # text: text to speak
    # engine: (optional) TTS engine to use. see ttsinfo()
    # language: (optional) language
    # pitch: (optional) pitch
    # rate: (optional) rate
    # stream: (optional) audio stream to use
    # region: (optional) language region
    # variant: (optional) language variant 
    # for more info visit [termux wiki](https://wiki.termux.com/wiki/Termux-tts-speak)



# OPEN_AI_KEY = os.environ.get("OPENAI_API_KEY")



# Get the current working directory
cwd = os.getcwd()

url = "http://10.10.2.189:5000/motion"
arm_url = f"http://10.10.2.106/js?json="


def take_action(action):
    print(action)
    data = {'motion': f"{action}"}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return json.dumps({"status_code": f"{r.status_code}", "text": f"{r.text}"})

def arm_control(x,y,z,t,spd):
    print(f"{x},{y},{z},{t},{spd}")
    data = json.dumps({"T":104,"x":f"{x}","y":f"{y}","z":f"{z}","t":f"{t}","spd":f"{spd}"})
    url = arm_url + data
    response = requests.get(url)
    content = response.text
    print(content)


base_filename = Path('photo.jpg')

def take_photo():
    new_filename = base_filename.with_name(f"{base_filename.stem}_{datetime.now().strftime('%Y%m%d%H%M')}{base_filename.suffix}")
    print(new_filename)
    # file_path = os.path.join(Path("/data/data/com.termux/files/home/storage/downloads/dev/deebotbase"), new_filename)
    filepath = f"/data/data/com.termux/files/home/storage/downloads/dev/cleanbot/images/{new_filename}"
    termux.Camera.takephoto(0,filepath)
    return filepath

def resize_photo(filepath):
    im = Image.open(filepath)
    im = ImageOps.exif_transpose(im)
    im.thumbnail((1000,1000))
    im = im.rotate(0)
    im.save(filepath)

def survey():
    x = 0
    while x < 1:
        take_action("rotate_right")
        time.sleep(0.5)
        new_filename = base_filename.with_name(f"{base_filename.stem}_{datetime.now().strftime('%Y%m%d%H%M')}_{x}{base_filename.suffix}")
        print(new_filename)
        # file_path = os.path.join(Path("/data/data/com.termux/files/home/storage/downloads/dev/deebotbase"), new_filename)
        filepath = f"/data/data/com.termux/files/home/storage/downloads/dev/cleanbot/images/{new_filename}"
        termux.Camera.takephoto(0,filepath)
        x = x + 1
    x = x + 1
    take_action("rotate_right")
    new_filename = base_filename.with_name(f"{base_filename.stem}_{datetime.now().strftime('%Y%m%d%H%M')}_{x}{base_filename.suffix}")
    print(new_filename)
    # file_path = os.path.join(Path("/data/data/com.termux/files/home/storage/downloads/dev/deebotbase"), new_filename)
    filepath = f"/data/data/com.termux/files/home/storage/downloads/dev/cleanbot/images/{new_filename}"
    termux.Camera.takephoto(0,filepath)
    return filepath  

# survey()

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
          "text": """You are the navigation system of a simple robot, your job is to navigate an unknown indoor space given only images that are taken automatically from the front of the robot. 
        the goal is to find a dog while avoiding bumping into any obsticles and exploring the whole environment. always take a action and move the arm, and describe in detail what you see in the image in the style of a documentary"""
       
        }
      ]
    }
    ]

tools = [
    {
        "type": "function",
        "function": {
            "name": "take_action",
            "description": "When the user asks the robot to move.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The action must be one of the following csv: forward,backward,rotate_left,rotate_right.",
                    },
                },
                "required": ["action"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "arm_control",
            "description": "When the user asks the robot arm to move to a x,y,z location with t being the hand and spd being the speed it moves to this location",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "number",
                        "description": "The x coordinate to move, accepts value between -400 to 400",
                    },
                    "y": {
                        "type": "number",
                        "description": "The y coordinate to move, accepts value between -400 to 400",
                    },
                    "z": {
                        "type": "number",
                        "description": "The z coordinate to move, accepts value between -200 to 400",
                    },
                    "t": {
                        "type": "number",
                        "description": "The t number between 1.1 to 5.1",
                    },
                    "spd": {
                        "type": "number",
                        "description": "the speed to move to the new location, accepts value between 0.1 to 1.0",
                    },
                },
                "required": ["x","y","z","t","spd"],
            },
        },
    },
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
        "text": "whats my next action"
      }
    ]
  }

  messages.append(new_message) 
  response = client.chat.completions.create(
      model="gpt-4o",
      temperature=1,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      messages=messages,
      tools=tools,
      tool_choice="auto", 
  )

  response_message = response.choices[0].message
  tool_calls = response_message.tool_calls

  if tool_calls:
      print("FUNCTION CALLED")
      # Step 3: call the function
      # Note: the JSON response may not always be valid; be sure to handle errors
      available_functions = {
          "take_action": take_action,
          "arm_control": arm_control,
      }  # only one function in this example, but you can have multiple
      messages.append(response_message)
      print(response_message)
      #TTS(response_message.content)
      for tool_call in tool_calls:
          function_name = tool_call.function.name
          function_to_call = available_functions[function_name]
          function_args = json.loads(tool_call.function.arguments)
          if function_name == "take_action":
            function_response = function_to_call(
                action=function_args.get("action")
            )
          elif function_name == "arm_control":
            function_response = function_to_call(
                x=function_args.get("x"),
                y=function_args.get("y"),
                z=function_args.get("z"),
                t=function_args.get("t"),
                spd=function_args.get("spd"),
            )
          messages.append(
              {
                  "tool_call_id": tool_call.id,
                  "role": "tool",
                  "name": function_name,
                  "content": function_response,
              }
          )
      response= client.chat.completions.create(
          model="gpt-4o",
          messages=messages,
          max_tokens=100,
      )
      response_message = response.choices[0].message
      messages.append(response_message)
      print(response_message)
  else:
    response_message = response.choices[0].message
    messages.append(response_message)
    print(response_message)
    #TTS(response_message.content)
      # ai_response ={
      #             "role": "assistant",
      #             "content": [
      #                 {
      #                 "type": "text",
      #                 "text": f"{response_message.choices[0].message.content}"
      #                 }
      #             ]
      #             },

      # messages.append(ai_response)
      