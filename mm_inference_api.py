from catboost import CatBoostRegressor
from flask import Flask, request, jsonify
import pandas as pd


# Initialize the Flask app
app = Flask(__name__)

model = CatBoostRegressor()
model.load_model("mm_catboost_model.h5")

df_train = pd.read_parquet("tv_data_processed.parquet")

@app.route("/predict", methods=['POST'])
def predict():
    try:
        data = request.get_json()
        for k in data:
            if k not in model.feature_names_:
                return jsonify({'error': f"invalid feature: {k}"}), 500

        feature_values = []  
        for i, feature in enumerate(model.feature_names_):
            if feature in data:
                feature_values.append(data[feature])
            elif i in model.get_cat_feature_indices():
                feature_values.append("Dummy category") # The categorical NAN values were filled by this string
            else:
                feature_values.append(df_train[feature].mean())

        print(feature_values)
        prediction = model.predict(feature_values)
        result = {'prediction': float(prediction)}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run()