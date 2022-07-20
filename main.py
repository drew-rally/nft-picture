from collections import Counter
from PIL import ImageTk, Image
import argparse
import random
import json
import csv
import pandas as pd
import os
#update


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


json_csv("/Users/drewlevine/PycharmProjects/layering/csv/testrly.csv")



# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

file = open("/Users/drewlevine/PycharmProjects/layering/traits and rarities.json")
data = json.load(file)
num_of_traits = (len(data['traits']))
traits = data['traits']
probabilities = data['probs']

print(traits)

# Dictionary variable for each trait.
# Eech trait corresponds to its file name

"""hat_files = os.listdir('/Users/drewlevine/PycharmProjects/layering/shit NFTs/hat')

print(hat_files)
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


"""

TOTAL_IMAGES = 10  # Number of random unique images we want to generate

all_images = []


# A recursive function to generate unique image combinations

# base_trait is the triat being checked and required_trait is the trait needed
def conditional_trait(characters, required_characters, trait_prob, spotInList):
    if characters == required_characters:
        probabilities[trait_prob][spotInList] = 40

    else:
        probabilities[trait_prob][spotInList] = 0

    print(probabilities)



# to:do add conditional_trait optionality
def create_new_image():
    new_image = {}

    # For each trait category, select a random trait based on the weightings
    for trait in (data['traits']):
        #how do I check the most recently added trait
        try:
            # checks if the hat trait is red in
            conditional_trait(new_image['hat'], 'red',"stash-prob", 3)
        except:
            pass
        new_image[trait] = random.choices(traits[trait], probabilities[trait+'-prob'])[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


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


# creates a dictionary for each trait and creates nested dictionary for each trait then sets it to 0
trait_count = {}
for key, values in traits.items():
    print('Key :: ', key)
    trait_count[key] = {}
    if(isinstance(values, list)):
        for value in values:
            trait_count[key][value] = 0
    else:
        print(value)


# counts the number of times a trait was used
for values in all_images:
    for value in values:
        spec_value = values[value]
        if spec_value == 0:
            break

        if value == "tokenId":
            break

        else:
            trait_count[value][spec_value] +=1
    else:
        print(value)

print(trait_count)


#### Generate Metadata for all Traits
METADATA_FILE_NAME = 'metadata-all-traits.json';
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


def image_opener(trait_files, nft_dic):
    size = len(trait_files)
    trait = trait_files[:size - 6]
    varient = (nft_dic[trait])
    im = f"""/Users/drewlevine/PycharmProjects/layering/shit NFTs/{trait}/{varient}.png"""
            #/Users/drewlevine/PycharmProjects/layering/shit NFTs/back/main.png
    return im


#### Generate Images
#itirate throught the meta data for each nft
# item is meta-data for one nft
for item in all_images:
    """photos_dic = {}
    # run a for loop to document each trait
    im_count = 1
    for trait in traits:
        #photos_dic[1] = = Image.open((image_opener('hat_files', item)))
        photos_dic[im_count] = Image.open((image_opener('hat_files', item)))
        im_count += 1
        print(photos_dic)"""

    im1 = Image.open((image_opener('back_files', item))).convert("RGBA")
    im2 = Image.open((image_opener('bandana_files', item))).convert("RGBA")
    im3 = Image.open((image_opener('body_files', item))).convert("RGBA")
    im4 = Image.open((image_opener('skin_files', item))).convert("RGBA")
    im5 = Image.open((image_opener('mouth accessories_files', item))).convert("RGBA")
    #im6 = Image.open((image_opener('head accessory_files', item))).convert("RGBA")


    # Create each composite (Alpha composite im2 over im1)
    im1.paste(im2, (0, 0), mask=im2)
    im1.paste(im3, (0, 0), mask=im3)
    im1.paste(im4, (0, 0), mask=im4)
    #im1.paste(im5, (0, 0), mask=im5)
    #im1.paste(im6, (0, 0), mask=im6)

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
    token["attributes"].append(getAttribute("bandana", i["bandana"]))
    token["attributes"].append(getAttribute("body", i["body"]))
    token["attributes"].append(getAttribute("head accessory", i["head accessory"]))
    token["attributes"].append(getAttribute("mouth accessories", i["mouth accessories"]))
    token["attributes"].append(getAttribute("skin", i["skin"]))

    with open('metadata' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()

