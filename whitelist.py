import json

WHITELIST_JSON = "whitelist.json"

bot_owners = ["Your id"]
whitelist = []


with open(WHITELIST_JSON) as file:
    data = json.load(file)

for element in bot_owners:
  if str(element) not in str(whitelist):
    whitelist.append(str(element))

for element in data:
  if str(element["snowflake"]) not in str(whitelist):
    whitelist.append(str(element))