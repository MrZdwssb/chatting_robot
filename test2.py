import openai
from pathlib import Path
import time
import configparser

ANSI_COLOR_GREEN = "\x1b[32m"
ANSI_COLOR_RESET = "\x1b[0m"


# 从ini文件中读取api_key
# config = configparser.ConfigParser()
# config.read('config.ini')
# openai.api_key = config['openai']['ai_account_key']
openai.api_key = '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'

text = ""  # 设置一个字符串变量
turns = []  # 设置一个列表变量，turn指对话时的话轮
last_result = ""


def chatgpt(question):
    global text
    global turns
    global last_result

    prompt = text + "\nHuman: " + question

    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # 这里我们使用的是davinci-003的模型，准确度更高。
            prompt=prompt,  # 你输入的问题
            temperature=0.9,  # 控制结果的随机性，如果希望结果更有创意可以尝试 0.9，或者希望有固定结果可以尝试 0.0
            max_tokens=2048,  # 这里限制的是回答的长度，你可以可以限制字数，如:写一个300字作文等。
            top_p=1,
            # [控制字符的重复度] -2.0 ~ 2.0 之间的数字，正值会根据新 tokens 在文本中的现有频率对其进行惩罚，从而降低模型逐字重复同一行的可能性
            frequency_penalty=0,
            # [控制主题的重复度] -2.0 ~ 2.0 之间的数字，正值会根据到目前为止是否出现在文本中来惩罚新 tokens，从而增加模型谈论新主题的可能性
            presence_penalty=0
        )

        result = response["choices"][0]["text"].strip()
        last_result = result
        turns += [question] + [result]  # 只有这样迭代才能连续提问理解上下文

        if len(turns) <= 10:  # 为了防止超过字数限制程序会爆掉，所以提交的话轮语境为10次。
            text = " ".join(turns)
        else:
            text = " ".join(turns[-10:])

        return result
    except Exception as exc:  # 捕获异常后打印出来
        print(exc)


if __name__ == '__main__':

    # 将问题和回复记录下来，待结束后保存到文件中
    question_list = []
    answer_list = []
    while True:
        question = input(ANSI_COLOR_GREEN +
                         "\n请输入问题，若输入exit退出\n" + ANSI_COLOR_RESET)
        question_list.append(question)
        if question == "exit":
            break
        answer = chatgpt(question)
        answer_list.append(answer)
        print("AI: " + answer)
    # 保存到文件中
    timestamp = time.strftime("%Y%m%d-%H%M-%S", time.localtime())
    file_name = 'output/chat ' + timestamp + '.md'
    f = Path(file_name)
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as f:
        for q, a in zip(question_list, answer_list):
            f.write(f"question: {q}\nanswer: {a}\n\n")
    print(ANSI_COLOR_GREEN + "对话内容已保存到文件中: " + file_name + ANSI_COLOR_RESET)

