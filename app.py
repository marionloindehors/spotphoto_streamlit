#ICI ON BUILD NOTRE INTERFACE
import streamlit as st
import requests
from google.oauth2 import service_account
from google.cloud import storage
from PIL import Image
from io import BytesIO

st.title(" Welcome to Spot Photo 🔍 ")
st.subheader("A wonderful app to find your pictures and start to tell your stories")

query = st.text_input('Which photo are you looking for ?')
k = st.slider('Number of pictures to display', 1, 5, 3)


columns = st.columns(2)

columns[0].write('Model : Text to Text')
models_choice = ['all-mpnet-base-v2','clip-ViT-B-32']

columns[1].write('Model : Images to Text')

#model_choice = st.selectbox('Please select a model', ('all-mpnet-base-v2', 'clip-ViT-B-32'))

if query is not None and query != '':
    for i in range(0,2):
        params = dict(model_choice=models_choice[i], query=query, k=k, )

        spot_photo_api_url = 'https://spotphoto-clzpjlq7na-ew.a.run.app/recherche'
        #http://127.0.0.1:8000/recherche
        response = requests.get(spot_photo_api_url, params=params)

        if response.ok:
            #st.markdown(f'{response.json()}')

            #credentials = service_account.Credentials.from_service_account_file('')

            client = storage.Client()
            #client = storage.Client('possible-aspect-369317')
            bucket_name = 'bucket_image_flickr30k'

            bucket = client.get_bucket(bucket_name)

            blob_l =[]
            d = response.json()

            for image in d.keys() :
                blob = bucket.get_blob(image)
                blob_l.append(blob)

            rows = len(d.keys())
            for x in range(rows):
                blob_n = blob_l[x]
                img = Image.open(BytesIO(blob_n.download_as_bytes()))
                columns[i].image(img)
        else:
            columns[i].write(response.json())
