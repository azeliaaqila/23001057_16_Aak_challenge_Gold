from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import re
import pandas as pd

class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: "API For Cleansing Data, By Azel"),
        'version' : LazyString(lambda: "1.0.0"),
        'description' : LazyString(lambda: "API untuk Cleansing Data, oleh Azel"),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint": "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs./"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)

@swag_from("docs/text_cleansing_file.yml", methods = ['POST'])
@app.route('/text-cleansing-file',methods = ['POST'])
def text_cleansing_file():

    file = request.files.getlist('file')[0]

    df = pd.read_csv(file,encoding="ISO-8859-1")

    text = df.Tweet.to_list()

    cleaned_text = []
    for text in text:
        cleaned_text.append(re.sub(r'[^a-zA-Z0-9]', '', text))

        json_response = {
            'status_code' : 200,
            'description' : "Text yang telah diproses",
            'data' : cleaned_text,
        }

        response_data = jsonify(json_response)
        return response_data
    
    @swag_from("docs/text_cleansing.yml",methods =['POST'])
    @app.route('/text-cleansing', methods=['POST'])
    def text_cleansing():
        text = request.form.get('text')
        text_clean = re.sub(r'[^a-zA-Z0-9]', '', text)

        json_response = {
            'status_code' : 200,
            'description': "Text yang sudah diproses",
            'data_raw': text,
            'data_clean': text_clean
        }
        return json_response
    if __name__ == '__main__':
        app.run(debug=True)