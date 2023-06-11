import pandas as pd


def gen_date(df, col_str):
    temp = pd.to_datetime(df[col_str], utc=True)
    return temp.dt.tz_convert(None)


def process_foi_request(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame([data])

    # extracting public body ID to new column
    df["public_body_id"] = df["public_body"].apply(lambda dct: int(dct.get("id")) if dct is not None else pd.NA)

    # string na
    df.loc[df.refusal_reason == "n/a", "refusal_reason"] = pd.NA

    # converting columns to int
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
    # datetime columns
    cols = ["due_date", "created_at", "last_message"]
    for i in cols:
        df[i] = gen_date(df, i)

    # renaming columns
    df.rename(columns={"jurisdiction": "jurisdiction_id"}, errors="raise", inplace=True)
    df.rename(columns={"campaign": "campaign_id"}, errors="raise", inplace=True)

    # extracting ids from string
    df["jurisdiction_id"] = df["jurisdiction_id"].apply(lambda x: int(x.split("/")[-2]) if x is not None else pd.NA)
    df["campaign_id"] = df["campaign_id"].apply(lambda x: int(x.split("/")[-2]) if x is not None else pd.NA)

    # converting columns to int
    df["campaign_id"] = pd.to_numeric(df["campaign_id"], errors="coerce").astype(pd.Int64Dtype())

    # making sure df only contains integer NAs
    df = df.fillna(pd.NA)
    return df


def process_jurisdiction(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame([data["public_body"]])
    df = df[["id", "name"]]
    return df


def process_public_body(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame([data["public_body"]])
    df = df[["id", "name", "jurisdiction"]]
    df["jurisdiction"] = df["jurisdiction"].apply(lambda x: x["id"] if x is not None else pd.NA)
    df.rename(columns={"jurisdiction": "jurisdiction_id"}, inplace=True)
    return df


def process_messages(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(data["messages"])
    df["foi_request_id"] = df["request"].apply(lambda req: int(req.split("/")[-2]))

    df["sender_public_body_id"] = df["sender_public_body"].apply(
        lambda pb: int(pb.split("/")[-2]) if pb is not None else pd.NA
    )
    df["recipient_public_body_id"] = df["recipient_public_body"].apply(
        lambda pb: int(pb.split("/")[-2]) if pb is not None else pd.NA
    )

    df["sender_public_body_id"] = pd.to_numeric(df["sender_public_body_id"], errors="coerce").astype(pd.Int64Dtype())
    df["recipient_public_body_id"] = pd.to_numeric(df["recipient_public_body_id"], errors="coerce").astype(
        pd.Int64Dtype()
    )

    df["timestamp"] = gen_date(df, "timestamp")

    df = df[
        [
            "id",
            "foi_request_id",
            "sender_public_body_id",
            "recipient_public_body_id",
            "sent",
            "is_response",
            "is_postal",
            "kind",
            "status",
            "timestamp",
        ]
    ]

    return df


def process_campaigns(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df = df[["id", "name", "start_date", "active", "slug"]]

    df["start_date"] = gen_date(df, "start_date")

    return df
