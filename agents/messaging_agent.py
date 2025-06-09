import os
from twilio.rest import Client
from agents.deals import Opportunity
import http.client
import urllib
from agents.agent import Agent
from config import Config
import json

# Uncomment the Twilio lines if you wish to use Twilio

DO_TEXT = True
DO_PUSH = False
USE_WHATSAPP = True  # New flag for WhatsApp

class MessagingAgent(Agent):

    name = "Messaging Agent"
    color = Agent.WHITE

    def __init__(self):
        """
        Set up this object to either do push notifications via Pushover,
        or messaging via Twilio (SMS or WhatsApp),
        whichever is specified in the constants
        """
        self.log(f"Messaging Agent is initializing")
        if DO_TEXT:
            twilio_creds = Config.get_twilio_credentials()
            self.me_from = twilio_creds['from_number']
            self.me_to = twilio_creds['to_number']
            if USE_WHATSAPP:
                self.me_from = f"whatsapp:{self.me_from}"
                self.me_to = f"whatsapp:{self.me_to}"
            self.client = Client(twilio_creds['account_sid'], twilio_creds['auth_token'])
            # self.content_sid = twilio_creds.get('content_sid')  # Get template SID if exists
            self.log("Messaging Agent has initialized Twilio")
        if DO_PUSH:
            pushover_creds = Config.get_pushover_credentials()
            self.pushover_user = pushover_creds['user']
            self.pushover_token = pushover_creds['token']
            self.log("Messaging Agent has initialized Pushover")

    def message(self, text):
        """
        Send a message using the Twilio API (SMS or WhatsApp)
        """
        self.log("Messaging Agent is sending a message")
        if USE_WHATSAPP:
            # Use template for WhatsApp
            message = self.client.messages.create(
                from_=self.me_from,
                # content_sid=self.content_sid,
                # content_variables=json.dumps({
                #     "1": text  # Adjust variables based on your template
                # }),
                body=text,
                to=self.me_to
            )
        else:
            # Regular SMS or WhatsApp text message
            message = self.client.messages.create(
                from_=self.me_from,
                body=text,
                to=self.me_to
            )

    def push(self, text):
        """
        Send a Push Notification using the Pushover API
        """
        self.log("Messaging Agent is sending a push notification")
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
          urllib.parse.urlencode({
            "token": self.pushover_token,
            "user": self.pushover_user,
            "message": text,
            "sound": "cashregister"
          }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

    def alert(self, opportunity: Opportunity):
        """
        Make an alert about the specified Opportunity
        """
        text = f"Deal Alert! Price=${opportunity.deal.price:.2f}, "
        text += f"Estimate=${opportunity.estimate:.2f}, "
        text += f"Discount=${opportunity.discount:.2f} :"
        text += opportunity.deal.product_description[:10]+'... '
        text += opportunity.deal.url
        if DO_TEXT:
            self.message(text)
        if DO_PUSH:
            self.push(text)
        self.log("Messaging Agent has completed")
        
    
        