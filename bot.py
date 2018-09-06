import re
import smtplib
import time
from slackclient import SlackClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print('Logging in to the email server.. Please wait')

uname = 'sendcoffee2018@gmail.com'
pword = 'Noah201818!@'
count = 0
try:
    msg = MIMEMultipart()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(uname, pword)
    print('Login successful :)')
    
except:
    print('Login unsucessful please try again')
    raise TypeError('Cannot connect to server.\
 Please try again later or check source code')

token = 'xoxb-334803754180-393368417605-0kW93djkeHg1huYNaFwDHaHi'
slack_client = SlackClient(token)
starterbot_id = None

RTM_READ_DELAY = 0.5
EXAMPLE_COMMAND = ""
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel, uname, count):
    default_response = "Not sure what you mean. Try *{}*.".format('Order large capp with skim milk :)')
    response = None
    if command.startswith(EXAMPLE_COMMAND):    
        response = "Your order: *{}*.".format(command)
        print('Incoming command:', response,'|',command)
        
    if command.startswith('help'):
        response ='Please format your order like this: _Name, order, extras_. \
        *_Remember: You can type in whatever, so be careful_* *Example: Duncan, \
        small latte, skim*'
    
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
    msg['Subject'] = "Coffee order: |{}|.".format(count)
    msg.attach(MIMEText('\n' + command, 'plain'))
    text = msg.as_string()
    server.sendmail(uname, "upstairscoffee2018@gmail.com", text)
    
if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Coffee Bot online and running...")    
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel, uname, count)
                count = count + 1
                print(count)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
