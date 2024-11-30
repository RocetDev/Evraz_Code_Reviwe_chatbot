import os
import requests
import json
import promptBase

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
            raise Exception(f"PEngine: Request failed with status code: {response.status_code}")
        response_json = response.json()
        content = response_json.get('choices')[0].get("message").get('content')
        return content

    def check_main_structure_dir(self, structure):
        self.set_system_content('''Отвечайте на русском языке. Представь, что ты программист и архитектор it проектов с многоленим опытом.
            Тебе дали задачу, в чат тебе будут присылать проекты, а ты должен их проверить и выявить нарушения которые написаны в стандартах.
            Все ошибки ты должен оформлять в строгий отчет, где будут указаны все ошибки которые допустил сотрудник.
        ''')
        content = self.custom_query(promptBase.prompt_main_structure_project(structure))
        self.set_system_content('Отвечайте на русском языке.')
        return content
    