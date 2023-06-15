from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn
from dagster_pandas.constraints import ColumnConstraintViolationException, ColumnConstraint
import pandas as pd


class NullOrDateConstraint(ColumnConstraint):
    def __init__(self):
        message = "Value must be either null or a date"
        super(NullOrDateConstraint, self).__init__(error_description=message, markdown_description=message)

    def validate(self, dataframe, column_name):
        rows_with_unexpected_values = dataframe[
            ~(dataframe[column_name].isnull() | pd.to_datetime(dataframe[column_name], errors="coerce").notnull())
        ]

        if not rows_with_unexpected_values.empty:
            raise ColumnConstraintViolationException(
                constraint_name=self.name,
                constraint_description=self.error_description,
                column_name=column_name,
                offending_rows=rows_with_unexpected_values,
            )


class NullOrIntConstraint(ColumnConstraint):
    def __init__(self):
        message = "Value must be either null or an int"
        super(NullOrIntConstraint, self).__init__(error_description=message, markdown_description=message)

    def validate(self, dataframe, column_name):
        rows_with_unexpected_values = dataframe[
            ~(dataframe[column_name].isnull() | dataframe[column_name].astype(str).str.isdigit())
        ]

        if not rows_with_unexpected_values.empty:
            raise ColumnConstraintViolationException(
                constraint_name=self.name,
                constraint_description=self.error_description,
                column_name=column_name,
                offending_rows=rows_with_unexpected_values,
            )


FOIRequestDf = create_dagster_pandas_dataframe_type(
    name="FOIRequestDf",
    columns=[
        PandasColumn.integer_column("id", min_value=0),
        PandasColumn(
            "jurisdiction_id",
            constraints=[
                NullOrIntConstraint(),
            ],
        ),
        PandasColumn.string_column("refusal_reason"),
        PandasColumn.float_column("costs"),
        PandasColumn(
            "due_date",
            constraints=[
                NullOrDateConstraint(),
            ],
        ),
        PandasColumn.datetime_column("created_at"),
        PandasColumn.datetime_column("last_message"),
        PandasColumn.string_column("status"),
        PandasColumn.string_column("resolution"),
        PandasColumn.integer_column("user_id"),
        PandasColumn(
            "public_body_id",
            constraints=[
                NullOrIntConstraint(),
            ],
        ),
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
