--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

-- Started on 2022-11-21 15:46:07

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
-- TOC entry 212 (class 1259 OID 17652)
-- Name: phone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phone (
    id_phone integer NOT NULL,
    model character varying(50) NOT NULL,
    processor character varying(50) NOT NULL,
    memory integer NOT NULL,
    ram integer NOT NULL
);


ALTER TABLE public.phone OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 17651)
-- Name: phone_id_phone_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.phone_id_phone_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phone_id_phone_seq OWNER TO postgres;

--
-- TOC entry 3333 (class 0 OID 0)
-- Dependencies: 211
-- Name: phone_id_phone_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.phone_id_phone_seq OWNED BY public.phone.id_phone;


--
-- TOC entry 210 (class 1259 OID 17424)
-- Name: role_of_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_of_users (
    id_role integer NOT NULL,
    role character varying(50) NOT NULL
);


ALTER TABLE public.role_of_users OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 17423)
-- Name: role_of_users_id_role_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_of_users_id_role_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_of_users_id_role_seq OWNER TO postgres;

--
-- TOC entry 3334 (class 0 OID 0)
-- Dependencies: 209
-- Name: role_of_users_id_role_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_of_users_id_role_seq OWNED BY public.role_of_users.id_role;


--
-- TOC entry 214 (class 1259 OID 17695)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    lastname character varying(50) NOT NULL,
    firstname character varying(50) NOT NULL,
    patronymic character varying(50) NOT NULL,
    login character varying(50) NOT NULL,
    password character varying(150) NOT NULL,
    role_user integer NOT NULL,
    exist boolean DEFAULT true NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 17694)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 3335 (class 0 OID 0)
-- Dependencies: 213
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 3175 (class 2604 OID 17655)
-- Name: phone id_phone; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone ALTER COLUMN id_phone SET DEFAULT nextval('public.phone_id_phone_seq'::regclass);


--
-- TOC entry 3174 (class 2604 OID 17427)
-- Name: role_of_users id_role; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_of_users ALTER COLUMN id_role SET DEFAULT nextval('public.role_of_users_id_role_seq'::regclass);


--
-- TOC entry 3176 (class 2604 OID 17698)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 3325 (class 0 OID 17652)
-- Dependencies: 212
-- Data for Name: phone; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (5, '6.6" Смартфон realme 9 Pro', 'Snapdragon 695', 128, 8);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (6, '6.4" Смартфон Samsung Galaxy S21 FE', 'Snapdragon 888', 128, 6);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (14, '6.53" Смартфон Xiaomi Redmi 9A', ' MediaTek Helio G25', 32, 2);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (15, '6.5" Смартфон Poco M3 Pro', 'MediaTek Dimensity 700', 128, 6);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (16, '6.6" Смартфон Huawei P50 Pro', 'Snapdragon 888', 256, 8);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (17, '6.43" Смартфон Xiaomi Redmi Note 10', 'MediaTek Helio G95', 128, 6);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (18, '6.67" Смартфон Xiaomi Redmi Note 10', 'Snapdragon 732G', 128, 8);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (19, '6.8" Смартфон Samsung Galaxy S22 Ul', 'Exynos 2200', 256, 12);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (21, '6.43" Смартфон POCO M4 Pro 4G', 'MediaTek Helio G96', 256, 8);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (22, '6.53" Смартфон Xiaomi Redmi 9C NFC', 'MediaTek Helio G35', 64, 3);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (23, 'Новый телефон', 'Самый мощный 999', 256, 16);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (24, 'Новейший телефон', 'Всем процессорам процессор и вообще', 32, 1);
INSERT INTO public.phone (id_phone, model, processor, memory, ram) VALUES (1, '4.7" Смартфон Apple iPhone SE 2022', 'Apple A15 Bionic', 32, 12);


--
-- TOC entry 3323 (class 0 OID 17424)
-- Dependencies: 210
-- Data for Name: role_of_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.role_of_users (id_role, role) VALUES (1, 'Администратор');
INSERT INTO public.role_of_users (id_role, role) VALUES (2, 'Пользователь');


--
-- TOC entry 3327 (class 0 OID 17695)
-- Dependencies: 214
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users (user_id, lastname, firstname, patronymic, login, password, role_user, exist) VALUES (1, 'Вершинин', 'Алексей', 'Александрович', 'admin', 'b''$2b$12$.VNgIrLBzX8TQ1FO/JqXgu8Lok2mpQLJJq7tbpPf2KeQZYucWBY6y''', 1, true);
INSERT INTO public.users (user_id, lastname, firstname, patronymic, login, password, role_user, exist) VALUES (2, 'Пупкин', 'Василий', 'Геннадьевич', 'user', 'b''$2b$12$8zhGaRE2qEp..2kFJfZwLeggD8mK6JYm2k8HOP.10eZrnKqdhec8S''', 2, true);
INSERT INTO public.users (user_id, lastname, firstname, patronymic, login, password, role_user, exist) VALUES (3, 'Петров', 'Василий', 'Викторович', 'petrov86', 'b''$2b$12$OBh6hFj9RGQ5v.O3xgEIkOakC0nos0CvZ/c532PReAjAjoWTXPSRm''', 2, false);


--
-- TOC entry 3336 (class 0 OID 0)
-- Dependencies: 211
-- Name: phone_id_phone_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.phone_id_phone_seq', 24, true);


--
-- TOC entry 3337 (class 0 OID 0)
-- Dependencies: 209
-- Name: role_of_users_id_role_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_of_users_id_role_seq', 2, true);


--
-- TOC entry 3338 (class 0 OID 0)
-- Dependencies: 213
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 3, true);


--
-- TOC entry 3181 (class 2606 OID 17657)
-- Name: phone phone_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_pkey PRIMARY KEY (id_phone);


--
-- TOC entry 3179 (class 2606 OID 17429)
-- Name: role_of_users role_of_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_of_users
    ADD CONSTRAINT role_of_users_pkey PRIMARY KEY (id_role);


--
-- TOC entry 3182 (class 2606 OID 17700)
-- Name: users users_role_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_user_fkey FOREIGN KEY (role_user) REFERENCES public.role_of_users(id_role);


-- Completed on 2022-11-21 15:46:07

--
-- PostgreSQL database dump complete
--

