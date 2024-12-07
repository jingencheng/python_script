import pyperclip
import time
from huggingface_hub import InferenceClient


class Qwen():
	def __init__(self, hist=[]):
		pass
	def communicate(self, ctnt):
		pass


class QwenFish(Qwen):
	def __init__(self, hist=[], prompt='', otpt=''):
		self.hist = hist # 提问纪录
		self.prompt = prompt
		self.otpt = otpt


	def communicate(self, ctnt):
		
		# 没有设置记忆能力 在messages里面
		if len(self.hist) > 7:
			self.hist = self.hist[-7:] # 保留最后7个提问记录

		self.hist.append(ctnt) # 保存提问纪录

		client = InferenceClient(api_key="+++++++++++++++++++++++++++++++++++") # access token here
		messages = [
			{"role": "system", "content": "You are a experienced writer. You are a helpful assistant."},
			{"role": "user", "content": self.prompt + ctnt}
		]
		stream = client.chat.completions.create(
			model="Qwen/Qwen2.5-Coder-32B-Instruct", 
			messages=messages, 
			max_tokens=500,
			stream=True
		)
		self.otpt = ''
		
		print("\n++++++++++++++++++ CHUNK ++++++++++++++++++++\n")
		for chunk in stream:
			self.otpt += chunk.choices[0].delta.content
			print(chunk.choices[0].delta.content, end="")
		print("\n+++++++++++++++++++++++++++++++++++++++++++++\n")


class TextExtractor:
    def __init__(self, marks='"'):
        self.marks = marks
    
    def extract(self, text):
        # This assumes that there is only one segment of text enclosed by the specified marks
        if len(text) == 0:
              return text
        ans_text = text.split(self.marks)
        ans_text = ans_text[1]

        return ans_text





who = "" # to ???
remain =  "" # which should remain <...>

qwen_key = QwenFish() # 抽取关键词
qwen = QwenFish() # initialize

qwen_extract = QwenFish() # 监管
te = TextExtractor() # 监管平替 模型sometimes有废话
print("请选中文本并复制(Command + C), 程序会自动抓取复制的内容:\n\n")


qwen_key = f"""
		Get keywords of the given text in the format ......
		"""

qwen.prompt = f"""
        I'd like you to look at the following text I wrote and edit it to make it sound more natural,formal and polite to a native English speaker. Do reasonable edits without changing the tone of the text {remain}, then output sentences. Please enclose the text in quotation marks. 
		"""
qwen_extract.prompt = f"""
		Output only the sentence inside the quotation marks, without the quotation marks.
		"""


previous_text = ""
pyperclip.copy("")  # 清空剪贴板

while True:
    try:
        # 检查当前剪贴板内容
        if pyperclip.paste() != te.extract(qwen.otpt):  
            current_text = pyperclip.paste()

            if current_text != previous_text:
                # 交互
                qwen.communicate(
                    f"""text: '''{current_text}''' """
                )
                previous_text = current_text  # 更新 previous_text

            # 更新剪贴板内容
            pyperclip.copy(te.extract(qwen.otpt))
            print(te.extract(qwen.otpt))
            print(f"""修改好的语句已复制到剪切板""")

        time.sleep(1)  # 每秒检查一次
    except KeyboardInterrupt:
        print("程序已终止。")
        break

















