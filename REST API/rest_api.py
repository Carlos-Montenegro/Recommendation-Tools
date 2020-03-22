#!/usr/bin/env python
# coding: utf-8

# # Recommendation REST API

# ## A Flask aplication to recommend items to a specific user based on precalculated file
# 
# In this notebook we build a flask API Endpoint that loads a csv file offline. The API has only one endpoint: /ratings/top. By calling (POST) this endpoint with a userId en optionally a count in the body, the top recommended items together with the prediction scores are returned.

# In[1]:


## Import packages
from flask import Flask, request, jsonify
import pandas


# In[ ]:


path="D:/User/Google Drive/Proyectos/Estudios/Maestría/Courses/17. Recommendation tools/Individual assignment"


# In[ ]:


app = Flask(__name__)
predictions = pandas.read_csv(path+"/predictions.csv").dropna().sort_values(['userId', 'prediction'], ascending=[True, False])

### Endpoint - one route /ratings/top - one HTTP verb = POST
@app.route("/ratings/top", methods=["POST"])
def top_ratings():
    ## read the body of the API call
    content = request.get_json()
    
    ## Interpretation of body
    if "userId" in content and type(content["userId"]) == int:
        userId = content["userId"]
    else:
        return "'userId' is required and should be an Integer."
        sys.exit("'userId' is required and should be an Integer.")
        
    if "count" in content and type(content["count"]) == int:
        count = content["count"]
    else:
        count = 5
    
    # filter predictions for the given userId
    predict = predictions[predictions.userId == userId].head(count)
    
    # select movieId, title and prediction and transform to list
    top_ratings = list(predict[["artist", "prediction"]].T.to_dict().values())
    
    # Return the result to the API
    return jsonify(top_ratings)

### Put endpoint online
if __name__ == '__main__':
    app.run(host='localhost', port=6000)


# In[ ]:




