from collections import Counter
from PIL import ImageTk, Image
import argparse
import random
import json
import csv
import pandas as pd
import os


def json_csv(csvFilePath):
    df = pd.read_csv(csvFilePath).fillna(0)
    # read in and count columns
    num_columns = (df.shape[1])

    trait_and_probs = {}
    traitdic = {}
    probsdic = {}

    col = 0
    # get columns names
    while col <= num_columns-1:
        trait_type = (df.columns[col])
        col +=2
        traitdic[trait_type] = []


    for trait in traitdic:
        traitdic[trait] = list(df[trait])

    col = 1
    while col <= num_columns-1:
        prop_type = (df.columns[col])
        col += 2
        probsdic[prop_type] = []

    for prob in probsdic:
        probsdic[prob] = list(df[prob])

    trait_and_probs = {"traits": traitdic,"probs": probsdic}

    with open("traits and rarities.json", 'w') as traits_file:
        json.dump(trait_and_probs, traits_file)
    traits_file.close()


json_csv("/Users/drewlevine/PycharmProjects/layering/csv/RLY.csv")



# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

file = open("/Users/drewlevine/PycharmProjects/layering/traits and rarities.json")
data = json.load(file)
num_of_traits = (len(data['traits']))
traits = data['traits']
probabilities = data['probs']





hat = ["black", "blue", "red"]
hair_weights = [30, 40, 15]

stash = ["black", "blue", "red", "orange"]
glasses_weights = [30, 40, 15, 0]

back = ["black", "blue", "red"]
stash_weights = [30, 40, 15, ]

# Dictionary variable for each trait.
# Eech trait corresponds to its file name

hat_files = {
    "black": "black-hair",
    "red": "red-hair",
    "blue": "blue-hair",
}

back_files = {
    "black": "black-back",
    "red": "red-back",
    "blue": "blue-back",
    "orange": "orange-back"

}

stash_files = {
    "black": "black-stash",
    "red": "red-stash",
    "blue": "blue-stash",
}




TOTAL_IMAGES = 10  # Number of random unique images we want to generate

all_images = []


# A recursive function to generate unique image combinations

# base_trait is the triat being checked and required_trait is the trait needed
def conditional_trait(characters, required_characters):
    if characters == required_characters:
        glasses_weights[3] = 40

    else:
        glasses_weights[3] = 0


def create_new_image():
    new_image = {}

    # For each trait category, select a random trait based on the weightings
    for trait in (data['traits']):
        new_image[trait] = random.choices(traits[trait], probabilities[trait+'-prob'])[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image

"""    new_image["hair"] = random.choices(hair, hair_weights)[0]
    conditional_trait(new_image["hair"], "black")
    new_image["glasses"] = random.choices(glasses, glasses_weights)[0]
    new_image["stash"] = random.choices(stash, stash_weights)[0]

if new_image in all_images:
    return create_new_image()
else:
    return new_image
"""

# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES):
    new_trait_image = create_new_image()

    all_images.append(new_trait_image)


# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


print("Are all images unique?", all_images_unique(all_images))

# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1

print(all_images)

# Get Trait Counts

hat_count = {}
for item in hat:
    hat_count[item] = 0

back_count = {}
for item in back:
    back_count[item] = 0

stash_count = {}
for item in stash:
    stash_count[item] = 0

for image in all_images:
    hat_count[image["back"]] += 1
    stash_count[image["stash"]] += 1
    back_count[image["hat"]] += 1

print("hat", hat_count, )
print("stash", stash_count)
print("back", back_count)

#### Generate Metadata for all Traits
METADATA_FILE_NAME = 'metadata-all-traits.json';
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


def image_opener(trait_files, nft_dic):
    size = len(trait_files)
    trait = trait_files[:size - 6]
    varient = (nft_dic[trait])
    im = f"""/Users/drewlevine/PycharmProjects/layering/shit NFTs/{trait}/{varient}-{trait}.png"""
    return im


#### Generate Images
for item in all_images:
    im1 = Image.open((image_opener('hat_files', item)))
    im2 = Image.open((image_opener('back_files', item)))
    im3 = Image.open((image_opener('stash_files', item)))

    # Create each composite (Alpha composite im2 over im1)
    im1.paste(im2, (0, 0), mask=im2)
    im1.paste(im3, (0, 0), mask=im3)

    # save images
    file_name = str(item["tokenId"]) + ".png"
    im1.save("/Users/drewlevine/PycharmProjects/layering/shit NFTs/images/" + file_name)

#### Generate Metadata for each Image

f = open('metadata-all-traits.json', )
data = json.load(f)

IMAGES_BASE_URI = "ADD_IMAGES_BASE_URI_HERE"
PROJECT_NAME = "ADD_PROJECT_NAME_HERE"


def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }


for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("back", i["back"]))
    token["attributes"].append(getAttribute("hat", i["hat"]))
    token["attributes"].append(getAttribute("stash", i["stash"]))

    with open('metadata' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()

