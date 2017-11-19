-- Table: public.xhamster_spider

-- DROP TABLE public.xhamster_spider;

CREATE TABLE public.xhamster_spider
(
  id bigint NOT NULL,
  title character varying,
  img_urls character varying[],
  categories character varying[],
  rating double precision,
  video_time integer,
  download_link character varying,
  myrate double precision,
  recommand_info double precision,
  CONSTRAINT xhamster_spider_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.xhamster_spider
  OWNER TO postgres;
