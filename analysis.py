import os
import json
import art
import operator
import string

from art.decor_dic import block1


def json_load(path):
    with open(path, "rb") as f:
        return json.load(f)


def sort_get(diction: dict):
    sorted_links = dict(sorted(diction.items(), key=operator.itemgetter(1), reverse=True))
    document = ''

    def write_line(txt):
        nonlocal document
        document += f'{txt}\n'

    for link in list(sorted_links.keys()):
        try:
            write_line(f"{str(link)}: {diction[link]}")
        except:
            write_line(f"Unknown: {diction[link]}")
    return document


def get_top(diction: dict):
    keys = dict(sorted(diction.items(), key=operator.itemgetter(1), reverse=True))

    for key in list(keys.keys()):
        return key


class PackageAnalysis:
    def __init__(self):
        self.attachments = 0
        self.words = {}
        self.links = {}
        self.favourite_channels = {}
        # self.best_friends = {} Removed because it would definitely create gossip (I can't be fucked to check the user ids)
        self.involved_gc = {}
        self.word_count = 0
        self.links_sent = 0
        self.pings_sent = 0
        self.spaces = 0

    def encode(self):
        # Turn the data into a readable file

        file = ""
        def write_line(text):
            nonlocal file
            file += f"{text}\n"

        write_line(f"{self.word_count} words")
        write_line(f"{self.attachments} attachments")
        write_line(f"{len(self.words)} unique words")
        write_line(f"{self.links_sent} links sent")
        write_line(f"{self.spaces} spaces")
        sorted_links = dict(sorted(self.links.items(), key=operator.itemgetter(1), reverse=True))
        write_line(art.text2art(text="LINKS SENT"))
        for link in list(sorted_links.keys()):
            try:
                write_line(f"{str(link)}: {sorted_links[link]}")
            except:
                write_line(f"Unknown: {sorted_links[link]}")

        write_line(art.text2art(text="USAGE OF WORDS"))
        write_line("Formatted as `{ WORD }: {AMOUNT}")

        sorted_words = dict(sorted(self.words.items(), key=operator.itemgetter(1), reverse=True))

        for word in list(sorted_words.keys()):
            try:
                write_line(f"{str(word)}: {self.words[word]}")
            except:
                write_line(f"Error whilst writing word, usage: {self.words[word]}")

        sorted_groups = dict(sorted(self.involved_gc.items(), key=operator.itemgetter(1), reverse=True))
        sorted_servers = dict(sorted(self.favourite_channels.items(), key=operator.itemgetter(1), reverse=True))

        write_line(art.text2art(text="GROUP CHATS"))

        for gc in sorted_groups.keys():
            try:
                write_line(f"{str(gc)}: {sorted_groups[gc]}")
            except:
                write_line(f"Error whilst writing group, usage: {sorted_groups[gc]}")

        write_line(art.text2art(text="SERVERS"))

        for gc in sorted_servers.keys():
            try:
                write_line(f"{str(gc)}: {sorted_servers[gc]}")
            except:
                write_line(f"Error whilst writing server, usage: {sorted_groups[gc]}")

        return file


def analyze(package_dir):
    package = PackageAnalysis()
    try:
        if os.path.exists(package_dir) and os.path.isdir(package_dir):
            messages_dir = os.path.join(package_dir, "messages")
            if os.path.exists(messages_dir):
                for folder in os.listdir(messages_dir):
                    data_folder = os.path.join(messages_dir, folder)
                    if os.path.isdir(data_folder):
                        messages_json = os.path.join(data_folder, "messages.json")
                        channel_json = os.path.join(data_folder, "channel.json")
                        message_score = 0

                        if os.path.exists(messages_json):
                            json_data = json_load(messages_json)
                            for message in json_data:
                                message_score += 10
                                if 'Contents' in message:
                                    new_message = ''
                                    link_block = ''
                                    for block in message['Contents'].split(" "):
                                        if not block.startswith('https://'):
                                            link_block += f"{block} "
                                    for symbol in list(link_block):
                                        if symbol == " ":
                                            package.spaces += 1
                                        if symbol in "\n\t ?.!|/()\"'{,}:;#\\":
                                            new_message += " "
                                        else:
                                            new_message += symbol
                                            message_score += .1

                                    words = new_message.split(" ")
                                    package.word_count += len(words)
                                    for hyperlink in message['Contents'].split(" "):
                                        message_score += 3
                                        # done differently
                                        if hyperlink.startswith("https://"):
                                            package.links_sent += 1
                                            if hyperlink in package.links:
                                                package.links[hyperlink] += 1
                                            else:
                                                package.links[hyperlink] = 1
                                    for word in words:
                                        if word != "":
                                            word = word.lower()
                                            if word.startswith("<@"):
                                                message_score += 20
                                                package.pings_sent += 1
                                            elif word.startswith("https://"):
                                                pass
                                            elif word in package.words:
                                                message_score += 1
                                                package.words[word] += 1
                                            else:
                                                message_score += 1
                                                package.words[word] = 1

                                if 'Attachments' in message:
                                    attachments = message['Attachments']
                                    if attachments != "":
                                        package.attachments += 1

                        if os.path.exists(channel_json):
                            json_data = json_load(channel_json)

                            if json_data['type'] == 'GUILD_TEXT':
                                key = json_data['guild']['name'] if 'guild' in json_data else json_data['id']
                                if key in package.favourite_channels:
                                    package.favourite_channels[key] += message_score
                                else:
                                    package.favourite_channels[key] = message_score
                            elif json_data['type'] == 'GROUP_DM':

                                if not 'name' in json_data:
                                    member_count = 0
                                    if 'recipients' in json_data:
                                        member_count = len(json_data['recipients'])
                                    key = f"Untitled GC with {member_count} members (id: {json_data['id']})"
                                else:
                                    key = json_data['name']
                                if key in package.involved_gc:
                                    package.involved_gc[key] += message_score
                                else:
                                    package.involved_gc[key] = message_score



    except Exception as e:
        return None, f'Critical Error!\n{e}'

    return package, 'No Errors!'
