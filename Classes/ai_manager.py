import os
from pathlib import Path

import yaml
from openai import OpenAI
from Classes import file_manager


class AiManager:
    def __init__(self, config_path='Resources/config.yaml'):
        # 获取当前文件所在目录
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        # 配置文件的绝对路径
        config_path = str(current_dir.parent / config_path)
        self.config = self.load_config(config_path)
        self.openai_base_url = os.getenv('OPENAI_BASE_URL', self.config['openai']['base_url'])
        self.openai_api_key = os.getenv('OPENAI_API_KEY', self.config['openai']['api_key'])
        self.context = self.config['app']['context']
        self.question = self.config['app']['question']
        self.filter_list = self.config['app']['filter_list']
        self.replacement = self.config['app']['replacement']
        self.role_description = self.config['app']['role_description']

    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def filter_and_replace(self, original_string):
        for item in self.filter_list:
            original_string = original_string.replace(item, self.replacement)
        return original_string

    def generate_letter(self, job_desc):
        langchain_prompt_template = f"""
        {self.role_description}

        工作描述
        {job_desc}

        简历内容:
        {self.context}

        要求:
        {self.question}
        """

        print('========================开始念咒========================')

        client = OpenAI(api_key=self.openai_api_key, base_url=self.openai_base_url)
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": langchain_prompt_template}],
            stream=True,
        )

        letter = ""

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                letter += chunk.choices[0].delta.content

        print('========================咒语生成========================')

        if len(letter) < 10:
            print("生成失败")
            return None

        letter = self.filter_and_replace(letter)

        file_manager.write_send_record(langchain_prompt_template + "\n\n\n\n" + letter)

        return letter
