import requests
import json
import os
import time

class selfbot:
    def __init__(self, token):
        self.__class__.token = token
        self.__class__.header = {"authorization": self.token}
        self.__class__.reactions = {":smiley:": "%F0%9F%98%83", ":grinning:": "%F0%9F%98%80", ":sob:": "%F0%9F%98%AD", ":laughing:": "%F0%9F%98%86"}
        self.token = token
        self.header = {"authorization": self.token}
        self.reactions = {":smiley:": "%F0%9F%98%83", ":grinning:": "%F0%9F%98%80", ":sob:": "%F0%9F%98%AD", ":laughing:": "%F0%9F%98%86"}

    class get_channel:
        def __init__(self, id):
            self.channel_id = id


        def create_invite(self, max_age: int):
            url = f'https://discord.com/api/v9/channels/{self.channel_id}/invites'
            data = {"max_age": f"{max_age}"}

            r = requests.post(url, json=data, headers=selfbot.header)
            print(r.status_code)

            return r.json()['code']

        def delete_invite(self, invite):
            url = f'https://discord.com/api/v9/invites/{invite}'

            r = requests.delete(url, headers=selfbot.header)
            print(r.status_code) 

        
        def typing(self):
            url = f'https://discord.com/api/v8/channels/{self.channel_id}/typing'
            r = requests.post(url, headers=selfbot.header)

        def send_message(self, message):
            url = f'https://discord.com/api/v8/channels/{self.channel_id}/messages'
            data = {"content": message}

            r = requests.post(url, json=data, headers=selfbot.header)
            print(r.status_code)

            return r.json()['id']

        def delete_message(self, message_id):
            url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages/{message_id}"

            r = requests.delete(url, headers=selfbot.header)

            print(r.status_code)

        def react_to_message(self, messageId, reaction):
            url = f'https://discord.com/api/v9/channels/{self.channel_id}/messages/{messageId}/reactions/{reaction}/%40me?location=Message'
            r = requests.put(url, headers=selfbot.header)
            print(r.status_code)

        def get_messages(self, limit: int):
            url = f'https://discord.com/api/v9/channels/{self.channel_id}/messages?limit={limit}'
            r = requests.get(url, headers=selfbot.header)

            messages = json.loads(r.text)
            if 'The resource is being rate limited.' in str(messages):
                print('Rate limited: Waiting 5 seconds to continue')
                time.sleep(5)
                url = f'https://discord.com/api/v9/channels/{self.channel_id}/messages?limit={limit}'
                r = requests.get(url, headers=selfbot.header)   
                messages = json.loads(r.text)
          
            for message in messages:
              author = f"{message['author']['username']}#{message['author']['discriminator']}"
              content = message['content']
              #print(f'{author}: {content}')

            return messages
          
        def log_messages(self, messages, filename):
            open(filename, 'w+').close()
            log = open(filename,'a')
            for message in messages:
                author = message['author']['username'] + '#' + message['author']['discriminator']
                content = message['content']
                time = message['timestamp'].split('T')[0]
                line = f'{time} {author}: {content}'
                try:
                    log.write(line + '\n')
                except:
                    continue
            log.close()

    def ping_user(userId):
        return f'<@{userId}>'

    class get_user:
        def __init__(self, id):
            self.id = id
            self.user_id = id

        def send_message(self, message):
            data = {'content': message, 'recipient_id': self.id}

            r = requests.post(f'https://discord.com/api/v9/users/@me/channels', json=data, headers=selfbot.header)
            print(r.status_code)
            channel_id = r.json()['id']

            url = f'https://discord.com/api/v8/channels/{channel_id}/messages'
            data = {"content": message}

            r = requests.post(url, json=data, headers=selfbot.header)
            print(r.status_code)

            return r.json()['id']



    class get_guild:
        def __init__(self, id):
            self.guild_id = id
            self.id = id

        def get_all_channels(self):
            r = requests.get(f'https://discordapp.com/api/v9/guilds/{self.guild_id}/channels', headers=selfbot.header)

            channels = r.json()
            channels_ = []

            for channel in channels:
                if channel['type'] == 0:
                    channels_.append(channel['id'])

            channels = channels_

            return channels
                    
            
        def delete_all_channels(self):
            response = requests.get(f"https://discord.com/api/guilds/{self.guild_id}/channels", headers=selfbot.header)
            data = response.json()

            for channel in data:
                r = requests.delete(f"https://discord.com/api/v9/channels/{channel['id']}", headers=selfbot.header)

                if r.status_code == 200:
                    print(f'200 SUCCESS in deleting channel: {channel["name"]}')
                else:
                    print(f'{r.status_code} ERROR in deleting channel: {channel["name"]}')


        def create_channels(self, channels):
            url = f'https://discord.com/api/v9/guilds/{self.guild_id}/channels'

            if type(channels) == list:
                for channel in channels:
                    data = {"name": channel, "type": "0"}
                    r = requests.post(url, json=data, headers=selfbot.header)
                    print(r.status_code)
            else:
                data = {"name": channels}
                r = requests.post(url, json=data, headers=selfbot.header)
                print(r.status_code)

            return r.json()['id']

    def create_guild(self, guild_name):
        url = 'https://discord.com/api/v9/guilds'
        data = {"name": guild_name}

        r = requests.post(url, json=data, headers=selfbot.header)
        print(r.status_code)

        return r.json()['id']


