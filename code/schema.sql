--
-- PostgreSQL database dump
--

-- Dumped from database version 11.9 (Debian 11.9-0+deb10u1)
-- Dumped by pg_dump version 12.6 (Ubuntu 12.6-0ubuntu0.20.04.1)

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

--
-- Name: contract; Type: TABLE; Schema: public; Owner: ******, used as owner below
--

CREATE TABLE public.contract (
    address text NOT NULL,
    block_no integer,
    "timestamp" integer
);


ALTER TABLE public.contract OWNER TO owner;

--
-- Name: run; Type: TABLE; Schema: public; Owner: ******
--

CREATE TABLE public.run (
    contract_address text,
    name text,
    "time" double precision,
    result text,
    found boolean DEFAULT true,
    failed boolean DEFAULT false
);


ALTER TABLE public.run OWNER TO owner;

--
-- Name: contract contract_pkey; Type: CONSTRAINT; Schema: public; Owner: ******
--

ALTER TABLE ONLY public.contract
    ADD CONSTRAINT contract_pkey PRIMARY KEY (address);


--
-- Name: run run_name_key; Type: CONSTRAINT; Schema: public; Owner: ******
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_name_key UNIQUE (name);


--
-- Name: run run_contract_address_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ******
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_contract_address_fkey FOREIGN KEY (contract_address) REFERENCES public.contract(address);


--
-- PostgreSQL database dump complete
--

