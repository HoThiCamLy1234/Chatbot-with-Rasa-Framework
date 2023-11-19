
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import requests
from rasa_sdk.events import SlotSet


class ActionGreetUser(Action):

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_greet_user")

        return [UserUtteranceReverted()]


class ActionLocation(Action):

    def name(self) -> Text:
        return "action_location_distance_ticketprice_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        latest_intent = get_latest_intent(tracker)
        
        if latest_intent[0]:
            if latest_intent[1] =="hcm":
                dispatcher.utter_message("http://local/hcm")
            else: dispatcher.utter_message("http://local/nt")
        else: dispatcher.utter_message("http://local/thong+tin+chung")
        
        return []


class Actionule(Action):

    def name(self) -> Text:
        return "action_race_rules_and_regulations_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_intent = get_latest_intent(tracker)
        
        if latest_intent[0]:
            if latest_intent[1] == "hcm":
                dispatcher.utter_message("http://rule/hcm")
            else:
                dispatcher.utter_message("http://rule/nt")
        else:
            dispatcher.utter_message("http://rule/thong+tin+chung")
        return []

def get_latest_intent(tracker):
    latest_hcm_event = None
    latest_nt_event = None
    latest_qn_event = None

    for event in reversed(tracker.events):
        if event['event'] == 'user':
            intent_name = event['parse_data']['intent']['name']
            if intent_name == "hcm" and not latest_hcm_event:
                latest_hcm_event = event
            elif intent_name == "nt" and not latest_nt_event:
                latest_nt_event = event
            elif intent_name == "qn" and not latest_qn_event:
                latest_qn_event = event

    # Xác định intent cuối cùng được gọi gần nhất
    latest_intent = max(
        (latest_hcm_event, "hcm"),
        (latest_nt_event, "nt"),
        (latest_qn_event, "qn"),
        key=lambda x: x[0]['timestamp'] if x[0] else 0
    )

    return latest_intent

class ActionUtterSighin(Action):
    def name(self) -> Text:
        return "utter_sighin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lưu trạng thái hiện tại vào slot
        tracker.slots["current_action"] = "utter_sighin"

        dispatcher.utter_message(
            "Bạn đã thực hiện đăng kí giải chạy chưa?",
            buttons=[
                {"title": "Chưa, Tôi cần tìm hiểu thông tin", "payload": "/dont_sighin"},
                {"title": "Hỗ trợ đăng kí, kiểm tra thanh toán", "payload": "/sup_sighin_payment_check"},
                {"title": "Quay lại để chọn giải khác", "payload": "/running"}
            ]
        )

        return []

class ActionBack(Action):
    def name(self) -> Text:
        return "action_back"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            "Bạn đã thực hiện đăng kí giải chạy chưa?",
            buttons=[
                {"title": "Chưa, Tôi cần tìm hiểu thông tin", "payload": "/dont_sighin"},
                {"title": "Hỗ trợ đăng kí, kiểm tra thanh toán", "payload": "/sup_sighin_payment_check"},
                {"title": "Quay lại để chọn giải khác", "payload": "/running"}
            ]
        )

        return []


# Tạo danh sách cho cá nhân
list_u = ["HCM2023U01", "HCM2023U02", "HCM2023U03"]

# Tạo danh sách cho nhóm
list_g = ["HCM2023G01", "HCM2023G02", "HCM2023G03"]

def check_payment_code_category(payment_code):
    if payment_code in list_u:
        return "cá nhân"
    elif payment_code in list_g:
        return "nhóm"
    else:
        return "Không thuộc danh sách cá nhân hoặc nhóm"


class ActionPaymentTransfer(Action):
    def name(self) -> Text:
        return "action_check_payment_transfer_tracker"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entitites = tracker.latest_message['entities']
        print("message", entitites)
        for e in entitites:
            if e['entity'] == 'payment_code':
                state = e['value']
        
        payment_code = next(tracker.get_latest_entity_values("payment_code"), None)
        category = check_payment_code_category(payment_code)
        
        if payment_code and category != "Không thuộc danh sách cá nhân hoặc nhóm":
            
            dispatcher.utter_message("Thanh toán thành công")
            dispatcher.utter_message(f"Mã thanh toán {payment_code} thuộc danh sách {category}.")
            
        else:
            dispatcher.utter_message(
                "Mã thanh toán của bạn không đúng hoặc không thuộc danh sách",
                buttons=[
                {"title": "Thử lại", "payload": "/transfer"},
                {"title": "Hủy bỏ", "payload": "/sup_sighin_payment_check"},
            ])
        return []
    
class ActionPerson(Action):
    def name(self) -> Text:
        return "action_personal_registration_tracker"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        latest_intent = get_latest_intent(tracker)
        
        if latest_intent[0]:
            if latest_intent[1] =="hcm":
                dispatcher.utter_message("http://dkperson/hcm")
            else: dispatcher.utter_message("http://dkperson/nt")
        else: dispatcher.utter_message("http://dkperson/thong+tin+chung")
        
        return []
    
class ActionGroud(Action):
    def name(self) -> Text:
        return "action_sign_up_for_group_tracker"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        latest_intent = get_latest_intent(tracker)
        
        if latest_intent[0]:
            if latest_intent[1] =="hcm":
                dispatcher.utter_message("http://dkgroud/hcm")
            else: dispatcher.utter_message("http://dkgroud/nt")
        else: dispatcher.utter_message("http://dkgroud/thong+tin+chung")
        
        return []