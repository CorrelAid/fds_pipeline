import pandas as pd


def process_foi_requests(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(data)

    # extracting public body ID to new column
    df["public_body_id"] = df["public_body"].apply(lambda dct: int(dct.get("id")) if dct is not None else pd.NA)

    # string na
    df.loc[df.refusal_reason == "n/a", "refusal_reason"] = pd.NA

    # converting user column to int
    df["user"] = df["user"].astype("float").astype(pd.Int64Dtype())

    # keeping only required columns
    df = df[
        [
            "id",
            "jurisdiction",
            "refusal_reason",
            "costs",
            "due_date",
            "created_at",
            "last_message",
            "status",
            "resolution",
            "user",
            "public_body_id",
            "campaign",
        ]
    ]

    # renaming columns
    df.rename(columns={"jurisdiction": "jurisdiction_id"}, errors="raise", inplace=True)
    df.rename(columns={"campaign": "campaign_id"}, errors="raise", inplace=True)

    # extracting ids from string
    df["jurisdiction_id"] = df["jurisdiction_id"].apply(lambda x: int(x.split("/")[-2]) if x is not None else pd.NA)
    df["campaign_id"] = df["campaign_id"].apply(lambda x: int(x.split("/")[-2]) if x is not None else pd.NA)

    # making sure df only contains integer NAs
    df = df.fillna(pd.NA)

    return df
