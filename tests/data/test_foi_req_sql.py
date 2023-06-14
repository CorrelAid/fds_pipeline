sql = (
    "INSERT INTO foi_requests (id, jurisdiction_id, refusal_reason, costs, due_date, created_at, last_message, status,"
    " resolution, user, public_body_id, campaign_id) VALUES ('46', '1', '', '0.0', NULL, '2011-08-01 21:34:45.784280',"
    " '2011-08-01 21:34:45.784280', 'asleep', NULL, NULL, '23', '10') ON CONFLICT (id) DO UPDATE SET id = '46',"
    " jurisdiction_id = '1', refusal_reason = '', costs = '0.0', due_date = NULL, created_at = '2011-08-01"
    " 21:34:45.784280', last_message = '2011-08-01 21:34:45.784280', status = 'asleep', resolution = NULL, user = NULL,"
    " public_body_id = '23', campaign_id = '10';"
)
