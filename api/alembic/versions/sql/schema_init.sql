--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2 (Debian 12.2-2.pgdg100+1)
-- Dumped by pg_dump version 12.2 (Debian 12.2-2.pgdg100+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET search_path = public, pg_catalog;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: researcher; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.researcher (
    email character varying(120) NOT NULL,
    "firtName" character varying(128),
    "lastName" character varying(128),
    id bigint NOT NULL
);


--
-- Name: researcher_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.researcher_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: researcher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.researcher_id_seq OWNED BY public.researcher.id;


--
-- Name: researcher id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.researcher ALTER COLUMN id SET DEFAULT nextval('public.researcher_id_seq'::regclass);


--
-- Name: researcher researcher_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.researcher
    ADD CONSTRAINT researcher_email_key UNIQUE (email);


--
-- Name: researcher researcher_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.researcher
    ADD CONSTRAINT researcher_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

