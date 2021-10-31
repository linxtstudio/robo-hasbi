import re

f = open("loker_raw_text.txt", "r")
raw_text = f.read()

filtered_text = re.sub(r"#(\w+)", "", raw_text, flags=re.IGNORECASE)

formated_text = filtered_text.replace("  ?", "?").replace("  ,", ",")


print(formated_text)