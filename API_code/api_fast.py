import tensorflow as tf
from tensorflow import keras
import cv2
import os
import uvicorn
import numpy as np
import tensorflow_hub as hub
from fastapi import FastAPI, File, UploadFile, HTTPException
import asyncio
import nest_asyncio

# Load model once at startup
custom_objects = {'KerasLayer': hub.KerasLayer}
model_path = "C:\\Users\\shrey\\OneDrive\\Desktop\\batanikaya_model_prototype.hdf5"

app = FastAPI()

plant_names = {
    'Aloevera-Aloe barbadensis': 0,
    'Amaranthus Green_Amaranthus viridis': 1,
    'Amaranthus Red_Amaranthus tricolor': 2,
    'Amla-Phyllanthus emlica Linn': 3,
    'Amruta Balli-Tinospora cordifolia': 4,
    'Arali-Nerium oleander': 5,
    'Arive_Dantu_Amaranthus viridis': 6,
    'Ashoka-Saraca asoca': 7,
    'Ashwagandha_Withania somnifera': 8,
    'Asthma plant_Euphorbia hirta': 9,
    'Astma_weed': 10,
    'Avacado_Persea americana': 11,
    'Avaram_Senna auriculata': 12,
    'Badipala': 13,
    'Balloon vine_Cardiospermum halicacabum': 14,
    'Bamboo-Bambusoideae': 15,
    'Basale_Basella alba': 16,
    'Beans-Vigna spp. (Genus) or Phaseolus spp. (Genus)': 17,
    'Bellyache bush (Green)_Jatropha gossypiifolia': 18,
    'Benghal dayflower_ Commelina benghalensis': 19,
    'Betel-Piper betle': 20,
    'Betel_Nut_Areca catechu': 21,
    'Big Caltrops_Tribulus terrestris': 22,
    'Black-Honey Shrub_Tribulus terrestris': 23,
    'Brahmi-Bacopa monnieri': 24,
    'Bringaraja-Eclipta prostrata': 25,
    'Bristly Wild Grape_Cissus quadrangularis': 26,
    'Butterfly Pea_Clitoria ternatea': 27,
    'Camphor-Cinnamomum camphora': 28,
    'Cape Gooseberry_Physalis peruviana': 29,
    'Cardiospermum halicacabum': 30,
    'Caricature': 31,
    'Castor-Ricinus communis': 32,
    'Catharanthus': 33,
    'Celery_Apium graveolens': 34,
    'Chakte': 35,
    'Chilly-Capsicum spp. (Genus)': 36,
    'Chinese Spinach_Amaranthus dubius': 37,
    'Citron lime (herelikai)-Citrus medica (Citron) or Citrus aurantiifolia (Lime)': 38,
    'coatbuttons_Tridax procumbens': 39,
    'Coffee-Coffea spp. (Genus)': 40,
    'Common rue(naagdalli)- Ruta graveolens': 41,
    'Common Wireweed_Sida rhombifolia': 42,
    'Coriander-Coriandrum sativum': 43,
    'Country Mallow_Abutilon indicum': 44,
    'crape Jasmine_Tabernaemontana divaricata': 45,
    'Crown flower_Calotropis gigantea': 46,
    'Curry Leaf-Murraya koenigii': 47,
    'Doddapatre-Plectanthus amboinicus': 48,
    'Drumstick- Moringa oleifera': 49,
    'Dwarf Copperleaf (Green)_Acalypha reptans': 50,
    'Dwarf copperleaf (Red)_ Acalypha wilkesiana': 51,
    'Ekka-Calotropis gigantea': 52,
    'Eucalyptus-Eucalyptus spp. (Genus)': 53,
    'False Amarnath_Digera muricata': 54,
    'Fenugreek Leaves_ Trigonella foenum-graecum': 55,
    'Ganigale': 56,
    'Ganike-Solanum nigrum': 57,
    'Gasagase-Grewia asiatica': 58,
    'Gauva-Psidium guajava': 59,
    'Geranium_ Pelargonium spp. (Genus)': 60,
    'Giant Pigweed_Amaranthus titan': 61,
    'Ginger-Zingiber officinale': 62,
    'Globe Amarnath-Gomphrena globosa': 63,
    'Gongura_Hibiscus sabdariffa': 64,
    'Green Chireta_Andrographis paniculata': 65,
    'heart-leaved moonseed_ Tinospora cordifolia': 66,
    'Henna-Lausonia inermis': 67,
    'Hibiscus-Hibiscus rosa sinensis': 68,
    'Holy Basil_ Ocimum sanctum': 69,
    'Honge-Milletia': 70,
    'indian Beech_Pongamia pinnata': 71,
    'Indian CopperLeaf_ Acalypha indica': 72,
    'Indian Jujube_Ziziphus mauritiana': 73,
    'Indian pennywort_Centella asiatica': 74,
    'Indian Sarsaparilla_Hemidesmus indicus': 75,
    'Indian Stinging Nettle_Urtica dioica subsp. gracilis': 76,
    'Indian Thornapple_Datura metel': 77,
    'Indian wormwood_Artemisia indica': 78,
    'Insulin': 79,
    'Ivy Gourd_Coccinia grandis': 80,
    'Jackfruit-Artocarpus heterophyllus': 81,
    'Jamaica Cherry-Gasagase_ Muntingia calabura': 82,
    'Jamun_Syzygium cumini': 83,
    'Jasmine-Jasmium': 84,
    'kamakasturi': 85,
    'Kambajala': 86,
    'Karanda_Carissa carandas': 87,
    'Kasambruga': 88,
    'kepala': 89,
    'Kohlrabi-Brassica oleracea var. gongylodes': 90,
    'Kokilaksha_Asteracantha longifolia': 91,
    'Lagos Spinach_Celosia argentea': 92,
    'Lambs Quarters_Chenopodium album': 93,
    'Land Caltrops (Bindii)_Tribulus cistoides': 94,
    'Lantana- Lantana camara': 95,
    'Lemon grass-Cymbopogon citratus': 96,
    'Lemon-Citrus limon': 97,
    'Lettuce Tree_Pisonia grandis': 98,
    'Madagascar Periwinkle_Catharanthus roseus': 99,
    'Madras Pea Pumpkin_Sesbania grandiflora': 100,
    'Malabar Catmint_Plectranthus amboinicus': 101,
    'Malabar_Nut-Justicia adhatoda': 102,
    'Malabar_Spinach-Basella alba': 103,
    'Mango_Mangifera indica': 104,
    'Marigold-Tagetes spp. (Genus)': 105,
    'Mexican Mint_Plectranthus amboinicus (also known as Cuban Oregano)': 106,
    'Mexican Prickly Poppy_Argemone mexicana': 107,
    'Mint-Mentha': 108,
    'Mountain Knotgrass_Aerva lanata': 109,
    'Mustard_Brassica juncea': 110,
    'Nagadali_Ruta graveolens': 111,
    'Nalta Jute_Corchorus olitorius': 112,
    'Neem_Azadirachta indica': 113,
    'Nelavembu-Andrographis paniculata': 114,
    'Nerale': 115,
    'Night blooming Cereus_Epiphyllum oxypetalum': 116,
    'Nithyapushpa_Vinca rosea': 117,
    'Nooni-Morinda citrifolia': 118,
    'Oleander_Nerium oleander': 119,
    'Onion-Allium cepa': 120,
    'Padri': 121,
    'Palak(Spinach)-Spinacia oleracea': 122,
    'Panicled Foldwing_Dicliptera paniculata': 123,
    'Pappaya-Carica papaya': 124,
    'Parijatha-Nyctanthes arbor-tristis': 125,
    'Pea-Pisum sativum': 126,
    'Peepal Tree_Ficus religiosa': 127,
    'Pepper-Piper nigrum': 128,
    'Pomegranate-Punica granatum': 129,
    'Prickly Chaff Flower_Achyranthes aspera': 130,
    'Pumpkin-Cucurbita pepo': 131,
    'Punarnava_Boerhavia diffusa': 132,
    'Purple Fruited Pea Eggplant_Solanum trilobatum': 133,
    'Purple Tephrosia_Tephrosia purpurea': 134,
    'Raddish-Raphanus sativus': 135,
    'Raktachandini_Pterocarpus santalinus': 136,
    'Rasna_Alpinia galanga': 137,
    'Rosary Pea_Abrus precatorius': 138,
    'Rose Apple_Syzygium jambos': 139,
    'Rose-Rosa': 140,
    'Roxburgh fig_Ficus auriculata': 141,
    'Sampige': 142,
    'Sandalwood_Santalum album': 143,
    'Sapota-Manikara zapota': 144,
    'Seethaashoka-Saraca asoca': 145,
    'Seethapala': 146,
    'Shaggy button weed_Diodia teres': 147,
    'Siru Keerai_Amaranthus tristis': 148,
    'Small Water Clover_Marsilea minuta': 149,
    'Spiderwisp_Cleome viscosa': 150,
    'Spinach1': 151,
    'Square Stalked Vine_Sarcostemma acidum': 152,
    'Stinking Passionflower_Passiflora foetida': 153,
    'Sweet Basil_Ocimum basilicum': 154,
    'Sweet flag_Acorus calamus': 155,
    'Tamarind_Tamarindus indica': 156,
    'Taro_Colocasia esculenta': 157,
    'Tecoma': 158,
    'Thumbe': 159,
    'Tinnevelly Senna_Cassia angustifolia (also known as Senna)': 160,
    'Tomato_Solanum lycopersicum': 161,
    'Trellis Vine_Cissus sicyoides': 162,
    'Trigonella Foenum-graecum (Fenugreek)': 163,
    'Tulasi-Ocimum sanctum_Ocimum sanctum (also known as Holy Basil)': 164,
    'Turmeric_ Curcuma longa': 165,
    'Velvet bean_Mucuna pruriens': 166,
    'Water Spinach_Ipomoea aquatica': 167,
    'Wood_sorel_ Oxalis spp': 168
}

plant_names_array = list(plant_names.keys())

def load_plant_detection_model():
    try:
        model = tf.keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)

        print("Model loaded successfully!")
        return model
    except OSError as e:
        print(f"Error loading model: {e}")
        return None

model = load_plant_detection_model()

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    try:
        bytes_data = await image.read()
        img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        preprocessed_image = preprocess_image(img)

        if model is None:
            raise HTTPException(status_code=500, detail="Failed to load model")

        prediction = model.predict(np.expand_dims(preprocessed_image, axis=0))
        plant_class_index = np.argmax(prediction)
        plant_name = plant_names_array[plant_class_index]

        return {"plant_name": plant_name}
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=400, detail="An error occurred during prediction")

def preprocess_image(img):
    resized_img = cv2.resize(img, (224, 224))
    normalized_img = resized_img / 255.0
    return normalized_img

if _name_ == "_main_":
    if "get_ipython" in dir():
        nest_asyncio.apply()
        config = uvicorn.Config(app, host="10.70.22.127", port=8080, log_level="info")
        server = uvicorn.Server(config)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(server.serve())
    else:
        uvicorn.run(app, host="10.70.22.127", port=8080, log_level="info")