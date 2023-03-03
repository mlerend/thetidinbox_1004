import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from thetidinbox_1004.main import (action_categories, pred_bertopic,
                                   pred_meeting_invit, pred_pro_perso,
                                   pred_spam, unique_values, urgent_categories)

app = FastAPI()

# Optional, good practice for dev purposes. Allow all middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
def index():
    return {'hello':'from the other side'}

@app.get("/all_functions")
def all_functions(test):
    test = pd.Series(test)
    spam = pred_spam(pd.DataFrame({"message": test})).tolist()
    pro_perso = pred_pro_perso(pd.DataFrame({"body": test})).tolist()
    urgent_class = urgent_categories(pd.DataFrame({"body": test}))['present']
    urgent_class = np.array(urgent_class.apply(lambda x : 1 if x else 0)).tolist()
    action_class = action_categories(pd.DataFrame({"body": test}))
    unique_action_class = np.array(unique_values(action_class['columnspresent'])).tolist()
    meeting = np.array(pred_meeting_invit(test)).tolist()
    topic = np.array(pred_bertopic(pd.DataFrame({"body": test}))).tolist()

    return {"spam prediction": spam,
            "pred_pro_perso": pro_perso,
            "urgent categorisation": urgent_class,
            "action categorisation": unique_action_class,
            "meeting prediction": meeting,
            "bertopic prediction": topic
            }
