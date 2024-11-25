# Plant Identification API

This API allows users to upload an image of a plant and receive the plant's name and a brief description of its medicinal uses.

## Requirements:

(Refer the Requirements file for the version information)
* Python
* TensorFlow
* Keras
* OpenCV-python
* Uvicorn
* nest_asyncio (if using Jupyter Notebook)
* Pillow
* httpx
* Google Cloud Generative AI Service (API Key required)

## Installation:

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Obtain a Google Cloud Generative AI Service API Key and set the `API_KEY` environment variable:

```bash
export API_KEY=YOUR_API_KEY
```

## Usage:

You can use run the code either using curl commands or in the VSCode Terminal directly.

1. Run the API server:

```bash
python BotAPI.py
```

   - This will start the API server on port `8050` by default.

2. Send a POST request to the `/predict` endpoint with a multipart form data containing an image file named `image`:

```
curl -X POST http://localhost:8050/predict -F "image=@plant.jpg"
```

   - Replace `plant.jpg` with the path to your image file.

The response will be a JSON object containing the following keys:

* `plant_name`: The predicted name of the plant.
* `description`: A brief description of the plant's medicinal uses.

## Preprocessing:

The API preprocesses the uploaded image by resizing it to a fixed size (224x224) and normalizing pixel values between 0 and 1.

## Model:

The plant identification model is a pre-trained deep learning model loaded from a HDF5 file (`batanikaya_model_prototype.hdf5`). This file is assumed to be located in the same directory as the script (`main.py`).

## Plant Descriptions:

Plant descriptions are generated using Google Cloud Generative AI Service. The API uses the `gemini-pro` model to generate a short description of the plant's medicinal uses based on the predicted plant name.

## Error Handling:

The API handles several potential errors including:

* Model loading failures
* Image reading errors
* Errors during prediction or description generation

In case of an error, the API returns an HTTP error code and a descriptive error message.

