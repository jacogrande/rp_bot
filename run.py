import os, time, json, random
from slackclient import SlackClient
from boto.s3.connection import S3Connection

BOT_TOKEN = os.environ["API_TOKEN"]

slack_client = SlackClient(BOT_TOKEN)
# starterbot's user ID in Slack: value is assigned after the bot starts up

BOT_ID = "UD1DEELAD"

# constants
AT_BOT = "<@" + BOT_ID + "	>"
FIREHOSE="C5AEQC2JD"
CHECK="check"
MONTHS = [False, "January","February","March","April","May","June","July","August","September","October","November","December"]

with open("songs.json", "r") as read_file:
    song_data = json.load(read_file)

with open("dates.json", "r") as read_file:
    date_data = json.load(read_file)

def refreshData():
    with open("songs.json", "r") as read_file:
        song_data = json.load(read_file)

def refreshDates():
    with open("dates.json", "r") as read_file:
        date_data = json.load(read_file)

def handle_command(command, channel):
    response = ""
    command = command.lower()
    command = command.split(" ")
    attachment = False

    if command[0] == "songs":
        refreshData()

        if len(command) > 1:
            sFilter = command[1].lower()
            sList = []
            found = False
            for song in song_data["songs"]:
                if song["G"].lower() == sFilter:
                    sList.append(song)
                    found = True
                elif song["G2"].lower() == sFilter:
                    sList.append(song)
                    found = True
                elif song["B"].lower() == sFilter:
                    sList.append(song)
                    found = True
                elif song["K"].lower() == sFilter:
                    sList.append(song)
                    found = True
                elif song["V"].lower() == sFilter:
                    sList.append(song)
                    found = True
                elif song["V2"].lower() == sFilter:
                    sList.append(song)
                    found = True
                elif song["D"].lower() == sFilter:
                    sList.append(song)
                    found = True

            inc = 0
            for song in sList:
                inc+=1
                sTitle = song["title"];
                sCast = [song["G"],song["G2"], song["B"], song["D"], song["K"], song["V"],song["V2"]]
                response = response +  "*" + str(inc) + ". " + sTitle + "*\n\tG: " + sCast[0] + " G2: " + sCast[1]  + " B: " + sCast[2] + " D: " + sCast[3] + " K: " + sCast[4] + " V: " + sCast[5] + " V2: " + sCast[6]+ "\n Status: " + song["Status"] + "\n";
            if found == False:
                response = sFilter + " has 0 songs"

        else:
            response = ""
            inc = 0
            for song in song_data["songs"]:
                inc+=1
                sTitle = song["title"];
                sCast = [song["G"],song["G2"], song["B"], song["D"], song["K"], song["V"],song["V2"]]
                response = response +  "*" + str(inc) + ". " + sTitle + "*\n\tG: " + sCast[0] + " G2: " + sCast[1]  + " B: " + sCast[2] + " D: " + sCast[3] + " K: " + sCast[4] + " V: " + sCast[5] + " V2: " + sCast[6]+ "\n\tStatus: " + song["Status"] + "\n";

    elif command[0] == "rehearsal" and command[1] == "list":
        refreshData()
        sList = []
        for song in song_data["songs"]:
            if song["Status"] == "Needs Work":
                sList.append(song)

        inc = 0
        for song in sList:
            inc+=1
            response = response + "*" + str(inc) + ". " + song["title"] + "*\n"

    elif command[0] == "calendar":
        refreshDates()
        dList = []
        dName = ""
        attachment = []
        color = False
        for date in date_data["dates"]:
            dName = date["date"].split("/")
            dName = MONTHS[int(dName[0])] + " " + dName[1]
            color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            attachment.append({
                "fallback":dName,
                "title":dName,
                "color":color,
                "fields": [
                    {
                        "title": "Location",
                        "value": date["location"],
                        "short": True
                    },
                    {
                        "title": "Time",
                        "value": date["time"],
                        "short": True
                    }
                ]
            })
        attachment = json.dumps(attachment)
        # attachment = False

    # elif command[0] == "set":
    #     if command[1] == "date":
    #

    elif command[0] == 'help':
        response = "Command List: \n\t- *songs* : displays song list"
        response += "\n\t- *songs* player_name : displays song list for player_name"
        response += "\n\t- *rehearsal list* : displays all songs that need work"
        response += "\n\t- *calendar* : displays upcoming show information"


    else:
        response = "Sorry, I don't understand (type *help* for help with commands)"

    if attachment == False:
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    else:
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True, attachments=attachment)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        if output_list[0]["type"] == "message" and output_list[0]["user"] != BOT_ID:
            return output_list[0]["text"], output_list[0]["channel"]
    return None, None

if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("socket to me...")
		while True:
			# retrieve the command and channel id from the parse_slack_output function
			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed... ")
