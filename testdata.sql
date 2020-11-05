--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: client; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.client (
    id integer NOT NULL,
    name character varying,
    address character varying(120),
    phone character varying(120)
);


--
-- Name: client_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.client_id_seq OWNED BY public.client.id;


--
-- Name: contractor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contractor (
    id integer NOT NULL,
    name character varying,
    phone character varying(120)
);


--
-- Name: contractor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.contractor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contractor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.contractor_id_seq OWNED BY public.contractor.id;


--
-- Name: job; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job (
    id integer NOT NULL,
    start_time timestamp without time zone,
    contractor_id integer NOT NULL,
    client_id integer NOT NULL
);


--
-- Name: job_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.job_id_seq OWNED BY public.job.id;


--
-- Name: client id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client ALTER COLUMN id SET DEFAULT nextval('public.client_id_seq'::regclass);


--
-- Name: contractor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contractor ALTER COLUMN id SET DEFAULT nextval('public.contractor_id_seq'::regclass);


--
-- Name: job id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job ALTER COLUMN id SET DEFAULT nextval('public.job_id_seq'::regclass);


--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.client (id, name, address, phone) FROM stdin;
1	Xineoh	1 Strouthos rd, Hyde Park	0114389710
2	Bvalgari	Shop U1, Hyde Park Corner	0114384590
3	Dunhill	1 William Nickel rd, Hyde Park	0114383654
4	Brave Group	18 Jan Smuts rd, Hyde Park	0114389812
\.


--
-- Data for Name: contractor; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.contractor (id, name, phone) FROM stdin;
1	Danie van Rensburg	0114384912
2	Petrus Coetzee	0834384912
3	Bertus Nienaber	0764384912
4	Arthur Pendragon	0654384912
\.


--
-- Data for Name: job; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.job (id, start_time, contractor_id, client_id) FROM stdin;
1	2020-11-10 12:00:00	1	1
2	2020-11-11 13:30:00	2	2
3	2020-11-12 14:45:00	3	3
4	2020-11-13 16:45:00	4	4
\.


--
-- Name: client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.client_id_seq', 4, true);


--
-- Name: contractor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.contractor_id_seq', 4, true);


--
-- Name: job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.job_id_seq', 4, true);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- Name: contractor contractor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contractor
    ADD CONSTRAINT contractor_pkey PRIMARY KEY (id);


--
-- Name: job job_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_pkey PRIMARY KEY (id);


--
-- Name: job job_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client(id) ON DELETE CASCADE;


--
-- Name: job job_contractor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_contractor_id_fkey FOREIGN KEY (contractor_id) REFERENCES public.contractor(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

