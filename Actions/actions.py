# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import datetime, time
import datetime as dt
import re
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from database_connection import dataUpdate

class ActionHelloWorld(Action): 
    def name(self): # type: () -> Text 
        return "action_check_working_hours"

    def run(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict[Text, Any]]
        cardinal_Val = str(tracker.get_slot('CARDINAL'))
        time_slot = str(tracker.get_slot('time_of_day'))
        section = str(tracker.get_slot('section_type'))
        names = str(tracker.get_slot('name_slot'))
        contact = str(tracker.get_slot('phone_slot'))
        

        if time_slot == 'a.m' or time_slot == 'am':
             message = 'We are not open at that time. We are only open from 7pm to 10pm. If you want to restart the conversation please feel free to tell the bot.'
             dispatcher.utter_message(message)
             return []
        
        if len(cardinal_Val)<=2 and time_slot=='pm' or time_slot=='p.m':
            hour = int(cardinal_Val)
            if hour > 7 and hour < 10:
                message = 'Thank you '+names+' for making your reservation at '+cardinal_Val+' '+time_slot+' in our '+section+' section. If you want to restart the conversation please feel free to tell the bot.'
                dataUpdate(names,contact,cardinal_Val,section)
            else:
                message = 'Sorry! we are not open at that time. Have a nice day! If you want to restart the conversation please feel free to tell the bot.'
            dispatcher.utter_message(message)
            return []
        
        if len(cardinal_Val)>2:
            split_time = re.split(":",cardinal_Val,maxsplit=1)
            hour = int(split_time[0])
            minutes = int(split_time[1])
            if hour > 7 and hour < 10:
                message = 'Thank you '+names+' for making your reservation at '+cardinal_Val+' '+time_slot+' in our '+section+' section. If you want to restart the conversation please feel free to tell the bot.'
                dataUpdate(names,contact,cardinal_Val,section)
            else:
                message = 'Sorry! we are not open at that time. Have a nice day! If you want to restart the conversation please feel free to tell the bot.'
            dispatcher.utter_message(message)
            return []

        print(time_slot)
        print(cardinal_Val)
        return []

class ActionRestarted(Action):

    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]

class ActionCustomFallback(Action):

     def name(self) -> Text:
         return "custom_fallback_action"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template('utter_ask_rephrase',tracker)

        return [UserUtteranceReverted()]

class ActionDefaultAskAffirmation(Action):

     def name(self) -> Text:
         return "action_default_ask_affirmation"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template('utter_ask_affirmation',tracker)

        return [UserUtteranceReverted()]

#class ActionDefaultFallback(Action):
#    def name(self) -> Text:
#        return "action_default_fallback"
#
#    def run(
#        self,
#        dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: Dict[Text, Any],
#    ) -> List[Dict[Text, Any]]:
#
#        # tell the user they are being passed to a customer service agent
#        dispatcher.utter_message(text="I am passing you to a human...")
#     
#        # pause the tracker so that the bot stops responding to user input
#        return [UserUtteranceReverted()]
#
#
#class ActionCustomFallback(Action):
#
#     def name(self) -> Text:
#         return "action_custom_fallback"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#        dispatcher.utter_template('utter_custom',tracker)
#
#        return [UserUtteranceReverted()]
# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
#class ActionSection(Action):
#
#     def name(self) -> Text:
#         return "action_section"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         
#         buttons = [
#             {"payload":'/AC{"section_type":"AC"}',"title":"AC"},
#             {"payload":'/NON-AC"{"section_type":"NON-AC"}',"title":"NON-AC"}
#         ]
#         dispatcher.utter_message(text="Which section would you like to reserve:",buttons=buttons)
#
#         return []
# 2 stage fallback action 
