CREATE TABLE events (
  world_id TEXT,
  topic_id TEXT,
  window_start TIMESTAMP,
  window_end TIMESTAMP,
  n_messages INTEGER,
  n_unique_hashes INTEGER,
  dup_rate DOUBLE,
  top_hashes TEXT,
  hash_concentration DOUBLE,
  burst_score DOUBLE,
  type_post DOUBLE,
  type_reply DOUBLE,
  type_retweet DOUBLE,
  time_histogram TEXT
);
