
CREATE TABLE practice_de.tracking (
  create_time timeuuid PRIMARY KEY,
  bid int,
  bn text,
  campaign_id int,
  cd int,
  custom_track text,
  de text,
  dl text,
  dt text,
  ed text,
  ev int,
  group_id int,
  id int,
  job_id int,
  md text,
  publisher_id int,
  rl text,
  sr text,
  ts timestamp,
  tz int,
  ua text,
  uid text,
  utm_campaign text,
  utm_content text,
  utm_medium text,
  utm_source text,
  utm_term text,
  v text,
  vp text
);

COPY practice_de.tracking (create_time, bid, bn, campaign_id, cd, custom_track, de, dl, dt, ed, ev, group_id, id, job_id, md, publisher_id, rl, sr, ts, tz, ua, uid, utm_campaign, utm_content, utm_medium, utm_source, utm_term, v, vp) FROM '/home/Cassandra/tracking.csv' WITH DELIMITER = ',' AND HEADER = TRUE;