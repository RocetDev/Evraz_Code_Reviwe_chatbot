import os
import requests
import json

class PEngine:
    def __init__(self, model_api, api_key, temperature=0.35, max_tokens=1024):
        self.model_api = model_api
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json; charset=utf-8"
        }

        self.system_prompt = {
            "role": "system",
            "content": "Отвечайте на русском языке."
        }

    def set_system_content(self, text):
        self.system_prompt['content'] = text

    def _prepare_data(self, user_input):
        data = {
            "model": "mistral-nemo-instruct-2407",
            "messages": [
                self.system_prompt,
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        return data

    def custom_query(self, text):
        data = self._prepare_data(text)
        response = requests.post(
            self.model_api,
            headers=self.headers,
            data=json.dumps(data)
        )
        if response.status_code != 200:
            raise Exception(f"Request failed with status code: {response.status_code}")
        response_json = response.json()
        content = response_json.get('choices')[0].get("message").get('content')
        return content

    def check_structure_dir(self, directory):
        pass