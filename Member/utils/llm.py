# llm_service.py

import requests
from django.conf import settings

# class LLMService:
#     def __init__(self):
#         self.api_url = "http://127.0.0.1:1234/v1/chat/completions"
#         self.model_name = "adityalavaniya_-_tinyllama-fitness-instructor"

#     def send_query(self, user_input):
#         payload = {
#             "model": self.model_name,
#             "messages": [
#                 {"role": "user", "content": user_input}
#             ],
#             "max_tokens": 500,
#             "temperature": 0.7
#         }

#         headers = {
#             "Content-Type": "application/json"
#         }

#         try:
#             response = requests.post(self.api_url, json=payload, headers=headers)
#             response.raise_for_status()

#             data = response.json()
#             answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")

#             return {
#                 "success": True,
#                 "response": answer
#             }

#         except requests.exceptions.HTTPError as http_err:
#             return {"success": False, "error": f"HTTP error: {str(http_err)}"}
#         except requests.exceptions.RequestException as req_err:
#             return {"success": False, "error": f"Request error: {str(req_err)}"}
#         except Exception as e:
#             return {"success": False, "error": f"Unexpected error: {str(e)}"}



class LLMService:
    def __init__(self):
        self.api_url = settings.API_URL
        self.model_name = settings.MODEL_NAME

    def send_query(self, user_input):
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": user_input}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")

            return {
                "success": True,
                "response": answer
            }

        except requests.exceptions.HTTPError as http_err:
            return {"success": False, "error": f"HTTP error: {str(http_err)}"}
        except requests.exceptions.RequestException as req_err:
            return {"success": False, "error": f"Request error: {str(req_err)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}



# #  #Standalone execution block
# if __name__ == "__main__":
    
#     print("LLM Service Standalone Test")
    
#     llm = LLMService()  # Uses default local URL and model name
#     print("Connected to:", llm.api_url)
#     print("Using model:", llm.model_name)

#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Exiting...")
#             break

#         result = llm.send_query(user_input)
#         if result["success"]:
#             print("AI:", result["response"])
#         else:
#             print("Error:", result["error"])