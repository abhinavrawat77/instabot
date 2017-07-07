from clarifai import rest
from clarifai.rest import ClarifaiApp
def get_keywords_from_image(url_of_image):

    app = ClarifaiApp(api_key='ecd67c30d8bc40d49dc25499fcb56862')
    model = app.models.get('general-v1.3')
    response = model.predict_by_url(url=url_of_image)
    return response