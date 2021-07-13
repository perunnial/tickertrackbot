-- Table: public.chatid_vs_tickers

-- DROP TABLE public.chatid_vs_tickers;

CREATE TABLE public.chatid_vs_tickers
(
    chatid integer NOT NULL,
    tickers text[] COLLATE pg_catalog."default",
    CONSTRAINT chatid_vs_tickers_pkey PRIMARY KEY (chatid)
)

TABLESPACE pg_default;

ALTER TABLE public.chatid_vs_tickers
    OWNER to postgres;