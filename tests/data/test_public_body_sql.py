sql = (
    "INSERT INTO public_bodies (id, name, jurisdiction_id) VALUES ('90', 'Bundesministerium für Ernährung und"
    " Landwirtschaft', '1') ON CONFLICT (id) DO UPDATE SET id = '90', name = 'Bundesministerium für Ernährung und"
    " Landwirtschaft', jurisdiction_id = '1';"
)