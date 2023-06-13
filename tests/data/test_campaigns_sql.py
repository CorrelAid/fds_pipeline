string = """INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('10', 'Prinzenfonds', '2020-06-18 08:00:00', 'False', 'prinzenfonds') ON CONFLICT (id) DO UPDATE SET id = '10', name = 'Prinzenfonds', start_date = '2020-06-18 08:00:00', active = 'False', slug = 'prinzenfonds';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('1', 'Frag den Bundestag', '2016-01-25 11:00:00', 'False', 'frag-den-bundestag') ON CONFLICT (id) DO UPDATE SET id = '1', name = 'Frag den Bundestag', start_date = '2016-01-25 11:00:00', active = 'False', slug = 'frag-den-bundestag';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('2', 'Frag das Jobcenter', '2016-10-20 10:00:00', 'False', 'frag-das-jobcenter') ON CONFLICT (id) DO UPDATE SET id = '2', name = 'Frag das Jobcenter', start_date = '2016-10-20 10:00:00', active = 'False', slug = 'frag-das-jobcenter';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('3', 'Gläserne Gesetze', '2017-06-15 10:00:00', 'False', 'glaserne-gesetze') ON CONFLICT (id) DO UPDATE SET id = '3', name = 'Gläserne Gesetze', start_date = '2017-06-15 10:00:00', active = 'False', slug = 'glaserne-gesetze';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('5', 'Frag sie Abi!', '2019-02-11 11:00:00', 'False', 'frag-sie-abi') ON CONFLICT (id) DO UPDATE SET id = '5', name = 'Frag sie Abi!', start_date = '2019-02-11 11:00:00', active = 'False', slug = 'frag-sie-abi';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('11', 'Spekulation abwenden', '2020-07-14 07:30:00', 'False', 'spekulation-abwenden') ON CONFLICT (id) DO UPDATE SET id = '11', name = 'Spekulation abwenden', start_date = '2020-07-14 07:30:00', active = 'False', slug = 'spekulation-abwenden';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('9', 'Glyphosat', '2019-04-02 08:00:00', 'False', 'glyphosat') ON CONFLICT (id) DO UPDATE SET id = '9', name = 'Glyphosat', start_date = '2019-04-02 08:00:00', active = 'False', slug = 'glyphosat';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('12', 'Black Box EU', '2020-11-15 12:17:00', 'False', 'blackboxeu') ON CONFLICT (id) DO UPDATE SET id = '12', name = 'Black Box EU', start_date = '2020-11-15 12:17:00', active = 'False', slug = 'blackboxeu';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('4', 'Topf Secret', '2019-01-14 11:00:00', 'True', 'topf-secret') ON CONFLICT (id) DO UPDATE SET id = '4', name = 'Topf Secret', start_date = '2019-01-14 11:00:00', active = 'True', slug = 'topf-secret';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('13', 'Klima-Gebäude-Check', '2020-09-25 12:53:00', 'False', 'klimacheck') ON CONFLICT (id) DO UPDATE SET id = '13', name = 'Klima-Gebäude-Check', start_date = '2020-09-25 12:53:00', active = 'False', slug = 'klimacheck';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('15', 'Verschlusssache Prüfung', '2021-01-26 11:00:00', 'True', 'verschlusssache-prufung') ON CONFLICT (id) DO UPDATE SET id = '15', name = 'Verschlusssache Prüfung', start_date = '2021-01-26 11:00:00', active = 'True', slug = 'verschlusssache-prufung';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('16', 'Aktion Ehrensache', '2021-03-16 08:56:00', 'False', 'aktion-ehrensache') ON CONFLICT (id) DO UPDATE SET id = '16', name = 'Aktion Ehrensache', start_date = '2021-03-16 08:56:00', active = 'False', slug = 'aktion-ehrensache';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('14', 'Mission Fleisch', '2020-12-08 00:00:00', 'False', 'topf-secret-mission-fleisch') ON CONFLICT (id) DO UPDATE SET id = '14', name = 'Mission Fleisch', start_date = '2020-12-08 00:00:00', active = 'False', slug = 'topf-secret-mission-fleisch';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('17', 'Lobbyregister selbst gemacht', '2021-06-07 06:00:00', 'False', 'lobbyregister-selbstgemacht') ON CONFLICT (id) DO UPDATE SET id = '17', name = 'Lobbyregister selbst gemacht', start_date = '2021-06-07 06:00:00', active = 'False', slug = 'lobbyregister-selbstgemacht';
INSERT INTO campaigns (id, name, start_date, active, slug) VALUES ('20', 'Lageberichte des Auswärtiges Amts', '2022-11-10 07:00:00', 'False', 'lageberichte-auswaertiges-amt') ON CONFLICT (id) DO UPDATE SET id = '20', name = 'Lageberichte des Auswärtiges Amts', start_date = '2022-11-10 07:00:00', active = 'False', slug = 'lageberichte-auswaertiges-amt';"""
