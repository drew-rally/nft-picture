import json
import random
import pandas as pd
from PIL import Image
#from comtypes.client import GetActiveObject


def json_csv(csvFilePath):
    df = pd.read_csv(csvFilePath).fillna(0)
    # read in and count columns
    num_columns = (df.shape[1])

    trait_and_probs = {}
    traitdic = {}
    probsdic = {}

    col = 0
    # get columns names
    while col <= num_columns - 1:
        trait_type = (df.columns[col])
        col += 2
        traitdic[trait_type] = []

    for trait in traitdic:
        traitdic[trait] = list(df[trait])

    col = 1
    while col <= num_columns - 1:
        prop_type = (df.columns[col])
        col += 2
        probsdic[prop_type] = []

    for prob in probsdic:
        probsdic[prob] = list(df[prob])

    trait_and_probs = {"traits": traitdic, "probs": probsdic}

    with open("traits and rarities.json", 'w') as traits_file:
        json.dump(trait_and_probs, traits_file)
    traits_file.close()


#json_csv("/Users/drewlevine/PycharmProjects/layering/csv/traits for script - ISSAC NEWTON Traits.csv")
#json_csv("/Users/drewlevine/PycharmProjects/layering/csv/traits for script - Alcapone.csv")
#json_csv("/Users/drewlevine/PycharmProjects/layering/csv/traits for script - AmeliaEarhart.csv")
#json_csv("/Users/drewlevine/PycharmProjects/layering/csv/traits for script - Big Brtoher.csv")
#json_csv("/Users/drewlevine/PycharmProjects/layering/csv/traits for script - Deaton.csv")
#json_csv("/Users/drewlevine/PycharmProjects/layering/csv/traits for script - RTR.csv")
json_csv("/Users/drewlevine/PycharmProjects/layering/csv/traits for script - Vangogh.csv")
# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

file = open("/Users/drewlevine/PycharmProjects/layering/traits and rarities.json")
data = json.load(file)
num_of_traits = (len(data['traits']))
traits = data['traits']
probabilities = data['probs']

# Dictionary variable for each trait.
# Eech trait corresponds to its file name

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
        # how do I check the most recently added trait
        try:
            # checks if the hat trait is red in
            conditional_trait(new_image['hat'], 'red', "stash-prob", 3)
        except:
            pass
        new_image[trait] = random.choices(traits[trait], probabilities[trait + '-prob'])[0]
        if new_image[trait] == 0:
            new_image.pop(trait, None)

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

#print("list of metadata for each NFT", all_images)

# trait count how much each trait was used
# creates a dictionary for each trait and creates nested dictionary for each trait then sets it to 0
trait_count = {}
for key, values in traits.items():
    trait_count[key] = {}
    for value in values:
        trait_count[key][value] = 0


# counts the number of times a trait was used
for values in all_images:
    for value in values:
        spec_value = values[value]
        if spec_value == 0:
            break

        if value == "tokenId":
            break

        else:
            trait_count[value][spec_value] += 1
    else:
        print(value)
with open('/Users/drewlevine/PycharmProjects/layering/metadata-count-NFTs.json' , 'w') as outfile:
    json.dump(trait_count, outfile, indent=4)


#### Generate Metadata for all Traits
METADATA_FILE_NAME = 'metadata-all-NFTs.json';
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


def image_opener(trait_files, nft_dic):
    if trait_files in nft_dic:
        varient = (nft_dic[trait_files])
        im = f"""/Users/drewlevine/PycharmProjects/layering/PHOF NFTs/traits/{trait_files}/{varient}.png"""
        # /Users/drewlevine/PycharmProjects/layering/PHOF NFTs/traits/back/main.png
        return im

    else:
        return None


# this function checks if the inputted trait is in the NFT then calls image_opener() with the correct inputs
# item is the metadat for one NFT
# trait is a category of variants i.e. (hats, skins, mouth accessorie)
def image_assigner(item, trait):
    if trait in item:
        im2 = Image.open((image_opener(trait, item))).convert("RGBA")
        # Create each composite (Alpha composite im2 over im1)
        im1.paste(im2, (0, 0), mask=im2)
        final2 = Image.new("RGBA", im2.size)
        final2 = Image.alpha_composite(final2, im1)
        final2 = Image.alpha_composite(final2, im2)
        im1.paste(final2, (0, 0), mask=final2)


def newton_layer():
    image_assigner(item, "Body")
    image_assigner(item, "Head")
    image_assigner(item, "Custom Accessory")
    image_assigner(item, "Eye Accessory")
    image_assigner(item, "Mouth Accessory")


def crop_image(coordinates, img):
    cropped_img = img.crop(coordinates)

    return cropped_img


# Generate Images
# heading in CSV file must be the same name as trait type next to item
# iterate through the metadata for each NFT
# item is meta-data for one nft
for item in all_images:
    #if 'Body' in item:
    im1 = Image.open((image_opener('back', item))).convert("RGBA")
    newton_layer()

    im1 = crop_image((176, 176, 1840, 1840), im1)
    file_name = str(item["tokenId"]) + ".png"
    im1.save("/Users/drewlevine/PycharmProjects/layering/PHOF NFTs/images/" + file_name)

# generates PNG with  frame and no background
for item in all_images:
    if 'back' in item:
        im1 = Image.open((image_opener('back', item))).convert("RGBA")
    newton_layer()


    file_name = str(item["tokenId"]) + ".PNG"
    im1.save("/Users/drewlevine/PycharmProjects/layering/PHOF NFTs/CMYK no background/" + file_name)

# generates PNG with  frame and background
for item in all_images:
    newton_layer()


    file_name = str(item["tokenId"]) + ".png"
    im1.save("/Users/drewlevine/PycharmProjects/layering/PHOF NFTs/CMYK background/" + file_name)

#### Generate Metadata for each Image

f = open('metadata-all-NFTs.json', )
data = json.load(f)

IMAGES_BASE_URI = "ADD_IMAGES_BASE_URI_HERE"
PROJECT_NAME = "ADD_PROJECT_NAME_HERE"


def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }


# reads metadata and creates pictures
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("back", i["back"]))
    token["attributes"].append(getAttribute("Body", i["Body"]))

    #conditonal checks if Custom Accessory exsists in "metadata-all-NFTs"
    if 'Custom Accessory' in i:
        token["attributes"].append(getAttribute("Custom Accessory", i["Custom Accessory"]))

    if 'Eye Accessory' in i:
        token["attributes"].append(getAttribute("Eye Accessory", i["Eye Accessory"]))

    if 'Head' in i:
        token["attributes"].append(getAttribute("Head", i["Head"]))

    if 'Mouth Accessory' in i:
        token["attributes"].append(getAttribute("Mouth Accessory", i["Mouth Accessory"]))

    with open('/Users/drewlevine/PycharmProjects/layering/metadata/metadata' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()

