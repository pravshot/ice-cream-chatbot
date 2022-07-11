# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


# action_ask_ic_type
# action_ask_ic_flavors
# validate_ic_form
# action_show_recommendations
# action_show_order_summary
# action_reset_slots

FLAVORS = ['vanilla', 'chocolate', 'strawberry', 'mint', 'rocky road']

class AskForICTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_ic_type"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        dispatcher.utter_message(
            text = "What type of ice cream would you like?",
            buttons = [
                {"title": "cup", "payload": "/cup"},
                {"title": "cone", "payload": "/cone"}
            ],
        )
        return []
    
class ResetSlotsAction(Action):
    def name(self) -> Text: 
        return "action_reset_slots"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]

class AskForICFlavorAction(Action):
    def name(self) -> Text:
        return "action_ask_ic_flavors"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        dispatcher.utter_message(
            text = f"What flavor of ice cream would you like? We have {', '.join(FLAVORS)}."
        )
        return []
    

class ShowRecommendationsAction(Action):
    def name(self) -> Text:
        return "action_show_recommendations"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cup_recommendation = "For cup ice cream, our best selling flavors are rocky road and strawberry."
        cone_recommendation = "For cone ice cream, our best selling flavors are chocolate and mint."
        if tracker.get_slot("ic_type") == "cup":
            dispatcher.utter_message(
                text = cup_recommendation
            )
        elif tracker.get_slot("ic_type") == "cone":
            dispatcher.utter_message(
                text = cone_recommendation
            )
        else:
            dispatcher.utter_message(
                text = cup_recommendation + " " + cone_recommendation
            )
        return []
    
class ShowOrderSummaryAction(Action):
    def name(self) -> Text:
        return "action_show_order_summary"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.get_slot("name")
        ic_type = tracker.get_slot("ic_type")
        ic_size = tracker.get_slot("ic_size")
        ic_flavors = tracker.get_slot("ic_flavors")
        if None in (name, ic_type, ic_size, ic_flavors):
            dispatcher.utter_message(
                text = "Sorry, the order is incomplete."
            )
        else:
            if ic_size == "small":
                dispatcher.utter_message(
                    text = f"Order Summary: A {ic_size} {ic_type} of ice cream with {ic_flavors[0]} for {name}."
                )
            elif ic_size == "large" and len(ic_flavors) == 1:
                dispatcher.utter_message(
                    text = f"Order Summary: A {ic_size} {ic_type} of ice cream with 2 scoops of {ic_flavors[0]} for {name}."
                )
            else:
                dispatcher.utter_message(
                    text = f"Order Summary: A {ic_size} {ic_type} of ice cream with 1 scoop of {ic_flavors[0]} and 1 scoop of {ic_flavors[1]} for {name}."
                )
        return []
    
class ValidateICForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_ic_form"
    
    def validate_name(self, slot_value: Any,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: DomainDict) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(
                text = "I didn't get that."
            )
            return {"name": None}
        else:
            dispatcher.utter_message(
                text = f"Hi, {slot_value}."
            )
            return {"name": slot_value}
        
    def validate_ic_type(self, slot_value: Any,
                         dispatcher: CollectingDispatcher,
                         tracker: Tracker,
                         domain: DomainDict) -> Dict[Text, Any]:
        if tracker.get_intent_of_latest_message() == "cup":
            dispatcher.utter_message(
                text = "Ok, Cup."
            )
            return {"ic_type": "cup"}
        elif tracker.get_intent_of_latest_message() == "cone":
            dispatcher.utter_message(
                text = "Ok, Cone."
            )
            return {"ic_type": "cone"}
        else:
            dispatcher.utter_message(
                text = "I didn't get that."
            )
            return {"ic_type": None}
    
    def validate_ic_size(self, slot_value: Any,
                         dispatcher: CollectingDispatcher,
                         tracker: Tracker,
                         domain: DomainDict) -> Dict[Text, Any]:
        
        if slot_value:
            dispatcher.utter_message(
                text = f"Ok, {slot_value}."
            )
            return {"ic_size": slot_value}
        else:
            dispatcher.utter_message(
                text = "I didn't get that. Maybe check phrasing/spelling."
            )
            return {"ic_size": None}
    
    def validate_ic_flavors(self, slot_value: Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: DomainDict) -> Dict[Text, Any]:
        # check for None
        if not slot_value or len(slot_value) == 0:
            dispatcher.utter_message(
                text = "There was an error. Please check spelling/phrasing."
            )
            return {"ic_flavors": None}
        # check for any invalid flavors
        if not any(flavor in FLAVORS for flavor in slot_value):
            dispatcher.utter_message(
                text = "I don't recognize that flavor(s). Please make sure you pick one of the flavors we have."
            )
            return {"ic_flavors": None}
        slot_value = set(slot_value)
        # check for number of flavors compared to size
        if len(slot_value) > 1 and tracker.get_slot("ic_size") == "small":
            dispatcher.utter_message(
                text = "You picked a small size which contains 1 scoop, but you picked multiple flavors. Please pick only 1 flavor."
            )
            return {"ic_flavors": None}
        if len(slot_value) > 2 and tracker.get_slot("ic_size") == "large":
            dispatcher.utter_message(
                text = "You picked a large size which contains 2 scoops, but you picked too many flavors. Please pick only 1 or 2 flavors."
            )
            return {"ic_flavors": None}
        # should be good at this point
        return {"ic_flavors": list(slot_value)}