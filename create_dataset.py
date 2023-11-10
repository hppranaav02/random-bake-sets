# Program to retrieve all assets from the page as a json dataset
import json
from fractions import Fraction
import re
import requests as req

md_file_url = "https://github.com/dpapathanasiou/recipes/raw/master/index/c/cookies.md"
json_file_url_prefix = "https://github.com/dpapathanasiou/recipes/raw/master/index"

response = req.get(md_file_url)
content = response.text


# Extract the url information from the main page
json_urls = []
pattern = r'\]\(([^)]+)\)'
matches = re.findall(pattern, content)
cleaned_links = [match.replace("../../index/", "") for match in matches]
for clean_link in cleaned_links:
    json_url = f"{json_file_url_prefix}/{clean_link}"
    json_urls.append(json_url)

def parse_mixed_fraction(mixed_fraction):
    if ' ' in mixed_fraction:
        # print(mixed_fraction)
        whole_part, fraction_part = mixed_fraction.split(' ')
        fraction = Fraction(fraction_part)
        return str(int(whole_part) + fraction)
    else:
        return mixed_fraction

recipes_data = {
    "recipes":[]
}

for url in json_urls:
  final_ingrs = []
  # get recipe from url
  res = req.get(url)
  data = res.json()

  # get name and ingridients from json
  name = data["title"]
  ingr = data["ingredients"]

  # Reformat the ingridients to required format
  for ing in ingr:
    # pattern = r'^([\d/]+)\s*([a-zA-Z]+)\s*(?:\([^)]+\))?\s*([^,]*)'
    pattern = r'^([\d\s/]+)\s*([a-zA-Z]+)\s*(?:\([^)]+\))?\s*([^,]*)'
    match = re.match(pattern, ing)

    if match:
        new_ingr = {
            "amount": parse_mixed_fraction(match.group(1).strip()),
            "unit": match.group(2),
            "ingridient":match.group(3).strip()
        }
        final_ingrs.append(new_ingr)

  recipe = {
      "title":name,
      "ingridients":final_ingrs
  }
  recipes_data["recipes"].append(recipe)

final_json_data = json.dumps(recipes_data,indent=2)
print(final_json_data)