from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
import pandas as pd
import joblib



app = FastAPI()

class UserInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    age: int = Field(..., description="Age of the person")
    workclass: str = Field(..., description="Workclass")
    fnlwgt: int = Field(..., description="Final weight")
    education_num: int = Field(..., alias="education.num", description="Education level encoded")
    marital_status: str = Field(..., alias="marital.status", description="Marital status")
    occupation: str = Field(..., description="Occupation")
    relationship: str = Field(..., description="Relationship status")
    race: str = Field(..., description="Race")
    sex: str = Field(..., description="Sex")
    capital_gain: int = Field(..., alias="capital.gain", description="Capital gain")
    capital_loss: int = Field(..., alias="capital.loss", description="Capital loss")
    hours_per_week: int = Field(..., alias="hours.per.week", description="Hours worked per week")
    native_country: str = Field(..., alias="native.country", description="Native country")

    def to_dataframe(self):
        data = self.model_dump(by_alias=True)
        df = pd.DataFrame([data])
        expected_columns = [
            "age",
            "workclass",
            "fnlwgt",
            "education.num",
            "marital.status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "capital.gain",
            "capital.loss",
            "hours.per.week",
            "native.country",
        ]
        return df[expected_columns]

model = joblib.load("pipeline.pkl")

@app.get("/")
def health():
    return {"status": "OK"}

@app.post("/predict")
def predict(payload: UserInput):
    result = model.predict(payload.to_dataframe())[0]
    if not result :
        return {"income":"<=50k"}
    else :
        return {"income":"<=50k"}



