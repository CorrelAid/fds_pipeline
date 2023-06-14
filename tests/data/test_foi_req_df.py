import pandas as pd
import numpy as np

data = {
    "id": [46],
    "jurisdiction_id": [1],
    "refusal_reason": [""],
    "costs": [0.0],
    "due_date": [pd.NaT],
    "created_at": ["2011-08-01 21:34:45.784280"],
    "last_message": ["2011-08-01 21:34:45.784280"],
    "status": ["asleep"],
    "resolution": [pd.NA],
    "user": [pd.NA],
    "public_body_id": 23,
    "campaign_id": 10,
}

df = pd.DataFrame(data)
