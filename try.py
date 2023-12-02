from configs import RAW_PROMPT
import re

data = '''{ '指令请回答菜品的原材料', '输入': '土豆豆角炖肉', '输出': '土豆2个，豆角100克，五花肉150克，生抽1勺，盐适量，五香粉或十三香适量，葱姜蒜适量，热水。' }
{ '指令': '请回答制作菜品时的诀窍', '输入': '土豆豆角炖肉', '输出': '火力不要太大，翻炒至土豆边发黄，豆角表面发皱即可盛出来。' }
{ '指令': '请回答肉炖的时间', '输入': '土豆豆角炖肉', '输出': '闷差不多20分钟。' }
]'''

def remove_non_chinese_digits(text):
    # 使用正则表达式匹配非数字和非中文字符并替换为空格
    cleaned_text = re.sub(r'[^\u4e00-\u9fff0-9]', '', text)
    return cleaned_text

a = data.split()
b = []

for i in range(len(a)):
    b.append(remove_non_chinese_digits(a[i]))

# filtered_list = [item for item in b if item.strip() != ""]

new_list = []
for item in b:
    if '输入' in item or '输出' in item or '指令' in item:
        index = re.search('输入', item)
        if index is None:
            index = re.search('输出', item)
        if index is None:
            index = re.search('指令', item)
        index = index.start()
        new_list.append(item[:index+2])
        try:
            new_list.append(item[index+2:])
        except Exception as e:
            pass

    else:
        new_list.append(item)

filtered_list = [item for item in new_list if item.strip() != ""]

print(filtered_list)