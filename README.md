# TV model

The following repo presents the whole workflow of the creation of a model, whose purpose is to predict TV prices. It has 3 main files:
* **mm_scraper.py**: python file which fetches data about TV from an online marketplace
* **model_build.ipynb**: Jupyter notebook, you can see the data preprocessing here, and the evaluation of several algorithms (catboost, logicstic regression, random forest) on the fetched dataset.
* **mm_inference_api.py**: The inference API for the previously created model. You can try it following the provided steps:
  *  To install the necessary python dependecnies use the following command: `pip install "pandas[parquet]" catboost flask`
  *  To start the REST API: `python mm_inference_api.py`
  *  The REST API should be exposed on the following endpoint: **localhost:5000/predict**
  *  You can invoke it with a POST request, and the body should contain key-values where key is a feature name, and value is the value for that feature. If an unknown feature is in the request, the API will return with 500, thus the request will be fail. Example request:
  ```json
    {
      "Termék típusa": "UHD Smart LED Televízió",
      "Kijelző típusa": "LED"
    }
 ```
  *  If it was succesfull the response's format will be the following:
```json
    {
      "prediction": 123456.78,
    }
 ```
