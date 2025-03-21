import os
import json
import wikipedia
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)

def get_podcast_summary(podcast_transcript):
    instructPrompt = """
    You are an expert copywriter who is responsible for publishing newsletters with thousands of subscribers. You recently listened to a great podcast
    and want to share a summary of it with your readers. Please write the summary of this podcast making sure to cover the important aspects that were
    discussed and please keep it concise.
    The transcript of the podcast is provided below.
    """
    request = instructPrompt + podcast_transcript
    chatOutput = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": request}
        ]
    )
    return chatOutput.choices[0].message.content

def get_podcast_guest(podcast_transcript):
    request = podcast_transcript[:10000]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "user", "content": request}
        ],
        functions=[
            {
                "name": "get_podcast_guest_information",
                "description": "Get information on the podcast guest using their full name and the name of the organization they are part of to search for them on Wikipedia",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "guest_name": {"type": "string", "description": "The full name of the guest who is speaking in the podcast"},
                        "guest_organization": {"type": "string", "description": "The full name of the organization that the podcast guest belongs to or runs"},
                        "guest_title": {"type": "string", "description": "The title, designation or role of the podcast guest in their organization"},
                    },
                    "required": ["guest_name"],
                },
            }
        ],
        function_call={"name": "get_podcast_guest_information"}
    )
    response_message = completion.choices[0].message

    podcast_guest = ""
    podcast_guest_org = ""
    podcast_guest_title = ""

    if 'function_call' in response_message:
        function_args = json.loads(response_message['function_call']['arguments'])
        podcast_guest = function_args.get("guest_name", "")
        podcast_guest_org = function_args.get("guest_organization", "")
        podcast_guest_title = function_args.get("guest_title", "")

    if podcast_guest:
        try:
            page = wikipedia.page(f"{podcast_guest} {podcast_guest_org} {podcast_guest_title}", auto_suggest=True)
            podcast_guest_summary = page.summary
        except wikipedia.exceptions.PageError:
            podcast_guest_summary = "Not Available"
        except wikipedia.exceptions.DisambiguationError as e:
            podcast_guest_summary = "Not Available"
    else:
        podcast_guest_summary = "Not Available"

    return {
        "name": podcast_guest,
        "org": podcast_guest_org,
        "title": podcast_guest_title,
        "summary": podcast_guest_summary
    }

def get_podcast_highlights(podcast_transcript):
    instructPrompt = """
    You are a podcast editor and producer. You are provided with the transcript of a podcast episode and have to identify the 5 most significant moments in the podcast as highlights.
    - Each highlight needs to be a statement by one of the podcast guests
    - Each highlight has to be impactful and an important takeaway from this podcast episode
    - Each highlight must be concise and make listeners want to hear more about why the podcast guest said that
    - The highlights that you pick must be spread out throughout the episode

    Provide only the highlights and nothing else. Provide the full sentence of the highlight and format it as follows -

    - Highlight 1 of the podcast
    - Highlight 2 of the podcast
    - Highlight 3 of the podcast
    """
    request = instructPrompt + podcast_transcript
    chatOutput = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": request}
        ]
    )
    return chatOutput.choices[0].message.content
