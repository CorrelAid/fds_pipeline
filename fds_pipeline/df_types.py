from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

FOIRequestDf = create_dagster_pandas_dataframe_type(
    name="FOIRequestDf",
    columns=[
        PandasColumn.integer_column("id", min_value=0),
        PandasColumn.integer_column("jurisdiction_id"),
        PandasColumn.string_column("refusal_reason"),
        PandasColumn.float_column("costs"),
        PandasColumn.datetime_column("due_date"),
        PandasColumn.datetime_column("created_at"),
        PandasColumn.datetime_column("last_message"),
        PandasColumn.string_column("status"),
        PandasColumn.string_column("resolution"),
        PandasColumn.integer_column("user"),
        PandasColumn.integer_column("public_body_id"),
        PandasColumn.integer_column("campaign_id"),
    ],
)

JurisdictionDf = create_dagster_pandas_dataframe_type(
    name="JurisdictionDf",
    columns=[
        PandasColumn.integer_column("id", min_value=0),
        PandasColumn.string_column("name"),
    ],
)

PublicBodyDf = create_dagster_pandas_dataframe_type(
    name="PublicBodyDf",
    columns=[
        PandasColumn.integer_column("id", min_value=0),
        PandasColumn.string_column("name"),
        PandasColumn.integer_column("jurisdiction_id", min_value=0),
    ],
)

CampaignDf = create_dagster_pandas_dataframe_type(
    name="CampaignDf",
    columns=[
        PandasColumn.integer_column("id", min_value=0),
        PandasColumn.string_column("name"),
        PandasColumn.string_column("slug"),
        PandasColumn.datetime_column("start_date"),
        PandasColumn.boolean_column("active"),
    ],
)

MessageDf = create_dagster_pandas_dataframe_type(
    name="MessageDf",
    columns=[
        PandasColumn.integer_column("id", min_value=0),
        PandasColumn.integer_column("foi_request_id"),
        PandasColumn.integer_column("sender_public_body_id"),
        PandasColumn.integer_column("recipient_public_body_id"),
        PandasColumn.boolean_column("sent"),
        PandasColumn.boolean_column("is_response"),
        PandasColumn.boolean_column("is_postal"),
        PandasColumn.string_column("kind"),
        PandasColumn.string_column("status"),
        PandasColumn.datetime_column("timestamp"),
    ],
)
