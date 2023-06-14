import pandas as pd
import re


def gen_date(df, col_str):
    temp = pd.to_datetime(df[col_str], utc=True, format="mixed")
    return temp.dt.tz_convert(None)


def process_foi_request(data) -> pd.DataFrame:
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


def process_public_body(data) -> pd.DataFrame:
    df = pd.DataFrame([data["public_body"]])
    try:
        df = df[["id", "name", "jurisdiction"]]
    except KeyError:
        raise KeyError("FOI request was not assigned a public body")
    df["jurisdiction"] = df["jurisdiction"].apply(lambda x: x["id"] if x is not None else pd.NA)
    df.rename(columns={"jurisdiction": "jurisdiction_id"}, inplace=True)
    return df


def process_messages(data) -> pd.DataFrame:
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


def process_campaigns(data) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df = df[["id", "name", "start_date", "active", "slug"]]
    df["start_date"] = gen_date(df, "start_date")
    return df


def process_jurisdictions(data) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df = df[["id", "name"]]
    return df


def gen_sql_insert_new(df, table_name) -> str:
    column_names = df.columns.tolist()
    values = df.values.tolist()
    query_lst = []
    for row in values:
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES "
        row_values = [f"'{str(value)}'" if pd.notnull(value) else "NULL" for value in row]
        value_string = f"({', '.join(row_values)})"
        query += value_string + " ON CONFLICT (id) DO UPDATE SET "
        update_values = [
            f"{column} = {value}" if pd.notnull(value) else f"{column} = NULL"
            for column, value in zip(column_names, row_values)
        ]
        query += ", ".join(update_values) + ";"
        query_lst.append(query)
    return "\n".join(query_lst)


def del_col(sql_string):
    # Find the campaign_id and its value in the SQL string
    campaign_id_match = re.search(r"campaign_id\s*=\s*'\d+'", sql_string)
    if campaign_id_match:
        campaign_id = campaign_id_match.group(0)
        campaign_id_value = re.search(r"\d+", campaign_id)
        campaign_id_value = f"'{campaign_id_value.group(0)}')"
        sql_string = sql_string.replace(campaign_id, "campaign_id = NULL")
        sql_string = sql_string.replace(campaign_id_value, "NULL)")
        sql_string = sql_string.rstrip(", ")
        sql_string = sql_string.lstrip(", ")

    return sql_string
