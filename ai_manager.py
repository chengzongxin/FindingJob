import os

from openai import OpenAI

import file_manager

# 从环境变量中读取值
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import yaml
from openai import OpenAI


# def generate_letter(job_desc):
#     # 读取配置文件
#     # 如果文件实际是 GBK 编码
#     with open('config.yaml', 'r', encoding='utf-8') as file:
#         config = file.read()
#
#     # 提取配置信息
#     context = config['letter_context']
#     question = config['letter_question']
#     character_limit = config['character_limit']
#
#     langchain_prompt_template = f"""
#     你将扮演一位求职者的角色,根据上下文里的简历内容以及应聘工作的描述,来直接给HR写一个亲切、礼貌、专业且字数严格限制在{character_limit}以内的求职消息,
#     要求能够用专业的语言结合简历中的经历和技能,并结合应聘工作的描述,来阐述自己的优势,尽最大可能打动招聘者。
#     始终使用中文来进行消息的编写。
#
#     工作描述
#     {job_desc}
#
#     简历内容:
#     {context}
#
#     要求:
#     {question}
#     """
#
#     print('========================开始念咒========================')
#
#     client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
#     stream = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": langchain_prompt_template}],
#         stream=True,
#     )
#
#     letter = ""
#
#     for chunk in stream:
#         if chunk.choices[0].delta.content is not None:
#             letter += chunk.choices[0].delta.content
#
#     print('========================咒语生成========================')
#
#     if len(letter) < 10:
#         print("生成失败")
#         return None
#
#     # 保存生成的结果
#     file_manager.write_send_record(langchain_prompt_template + "\n\n\n\n" + letter)
#
#     return letter

def generate_letter(job_desc):
    context = """
    您好，我叫程宗鑫，我对您发布的职位非常感兴趣，我有丰富的开发经验，尤其擅长iOS、前端、uni跨平台、微信小程序、鸿蒙等项目开发。也熟悉Flutter、iOS底层原理、逆向工程和后端技术。我热衷于钻研技术、分析和解决难题，特别是在团队增效技术方面有深入研究。曾在土巴兔公司工作，参与了多个大规模项目，使用了许多前沿技术，覆盖了市面上的大部分功能点。方便的话，我可以发简历给您看看。
    """

    question = """
    根据工作描述，寻找出简历里最合适的技能都有哪些?求职者的优势是什么?
    这是一份求职消息，
    不要出现"此致"、"敬礼"、“xxx”、"你的名字"等词语
    不要出现gpt的语气，不能让别人以为是gpt写的
    不要包含求职内容以外的东西,例如“根据您上传的求职要求和个人简历,我来帮您起草一封求职邮件：”这一类的内容，以便于我直接自动化复制粘贴发送。
    """

    # 字数限制
    character_limit = 300

    langchain_prompt_template = f"""
    你将扮演一位求职者的角色,根据上下文里的简历内容以及应聘工作的描述,来直接给HR写一个亲切、礼貌、专业且字数严格限制在{character_limit}以内的求职消息,
    要求能够用专业的语言结合简历中的经历和技能,并结合应聘工作的描述,来阐述自己的优势,尽最大可能打动招聘者。
    始终使用中文来进行消息的编写。

    工作描述
    {job_desc}

    简历内容:
    {context}

    要求:
    {question}
    """

    print('========================开始念咒========================')

    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": langchain_prompt_template}],
        stream=True,
    )

    # print(stream)

    letter = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            letter += chunk.choices[0].delta.content

    print('========================咒语生成========================')

    if len(letter) < 10:
        print("生成失败")
        return None

    file_manager.write_send_record(langchain_prompt_template + "\n\n\n\n" + letter)

    return letter
