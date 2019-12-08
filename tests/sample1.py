import os
import slack

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

response = client.chat_postMessage(
    channel='#random',
    text="Hello world!")
assert response["ok"]
assert response["message"]["text"] == "Hello world!"


import os
import slack

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

response = client.files_upload(
    channels='#random',
    file="my_file.pdf")
assert response["ok"]


import os
import slack

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'Hello' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            thread_ts=thread_ts
        )

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()