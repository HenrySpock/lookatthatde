--
-- PostgreSQL database dump
--

-- Dumped from database version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO kodai;

--
-- Name: feedback; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.feedback (
    id integer NOT NULL,
    user_id integer,
    user_email character varying(100) NOT NULL,
    content character varying(250),
    list_id integer,
    creator_id integer
);


ALTER TABLE public.feedback OWNER TO kodai;

--
-- Name: feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.feedback_id_seq OWNER TO kodai;

--
-- Name: feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.feedback_id_seq OWNED BY public.feedback.id;


--
-- Name: field_data; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.field_data (
    id integer NOT NULL,
    field_id integer NOT NULL,
    image_id integer NOT NULL,
    value character varying(255)
);


ALTER TABLE public.field_data OWNER TO kodai;

--
-- Name: field_data_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.field_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.field_data_id_seq OWNER TO kodai;

--
-- Name: field_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.field_data_id_seq OWNED BY public.field_data.id;


--
-- Name: fields; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.fields (
    id integer NOT NULL,
    name character varying,
    type character varying,
    list_id integer
);


ALTER TABLE public.fields OWNER TO kodai;

--
-- Name: fields_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.fields_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fields_id_seq OWNER TO kodai;

--
-- Name: fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.fields_id_seq OWNED BY public.fields.id;


--
-- Name: image; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.image (
    image_id integer NOT NULL,
    list_id integer NOT NULL,
    image_url character varying(255) NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.image OWNER TO kodai;

--
-- Name: image_image_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.image_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.image_image_id_seq OWNER TO kodai;

--
-- Name: image_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.image_image_id_seq OWNED BY public.image.image_id;


--
-- Name: image_list; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.image_list (
    list_id integer NOT NULL,
    name character varying(80) NOT NULL,
    description text,
    creator_id integer,
    category_id integer,
    core_list boolean
);


ALTER TABLE public.image_list OWNER TO kodai;

--
-- Name: image_list_list_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.image_list_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.image_list_list_id_seq OWNER TO kodai;

--
-- Name: image_list_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.image_list_list_id_seq OWNED BY public.image_list.list_id;


--
-- Name: image_position; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.image_position (
    id integer NOT NULL,
    image_id integer NOT NULL,
    list_id integer NOT NULL,
    "position" integer NOT NULL
);


ALTER TABLE public.image_position OWNER TO kodai;

--
-- Name: image_position_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.image_position_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.image_position_id_seq OWNER TO kodai;

--
-- Name: image_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.image_position_id_seq OWNED BY public.image_position.id;


--
-- Name: list_category; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.list_category (
    category_id integer NOT NULL,
    name character varying(80) NOT NULL,
    description text
);


ALTER TABLE public.list_category OWNER TO kodai;

--
-- Name: list_category_category_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.list_category_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.list_category_category_id_seq OWNER TO kodai;

--
-- Name: list_category_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.list_category_category_id_seq OWNED BY public.list_category.category_id;


--
-- Name: user_image; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.user_image (
    user_image_id integer NOT NULL,
    user_id integer NOT NULL,
    image_id integer NOT NULL,
    name character varying(80),
    description text,
    is_custom_added boolean NOT NULL
);


ALTER TABLE public.user_image OWNER TO kodai;

--
-- Name: user_image_user_image_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.user_image_user_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_image_user_image_id_seq OWNER TO kodai;

--
-- Name: user_image_user_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.user_image_user_image_id_seq OWNED BY public.user_image.user_image_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: kodai
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password_hash character varying(120) NOT NULL,
    email character varying(120) NOT NULL,
    is_admin boolean,
    first_name character varying(80),
    last_name character varying(80)
);


ALTER TABLE public.users OWNER TO kodai;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: kodai
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO kodai;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kodai
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: feedback id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.feedback ALTER COLUMN id SET DEFAULT nextval('public.feedback_id_seq'::regclass);


--
-- Name: field_data id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.field_data ALTER COLUMN id SET DEFAULT nextval('public.field_data_id_seq'::regclass);


--
-- Name: fields id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.fields ALTER COLUMN id SET DEFAULT nextval('public.fields_id_seq'::regclass);


--
-- Name: image image_id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image ALTER COLUMN image_id SET DEFAULT nextval('public.image_image_id_seq'::regclass);


--
-- Name: image_list list_id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image_list ALTER COLUMN list_id SET DEFAULT nextval('public.image_list_list_id_seq'::regclass);


--
-- Name: image_position id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image_position ALTER COLUMN id SET DEFAULT nextval('public.image_position_id_seq'::regclass);


--
-- Name: list_category category_id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.list_category ALTER COLUMN category_id SET DEFAULT nextval('public.list_category_category_id_seq'::regclass);


--
-- Name: user_image user_image_id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.user_image ALTER COLUMN user_image_id SET DEFAULT nextval('public.user_image_user_image_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.alembic_version (version_num) FROM stdin;
036cce8f3007
\.


--
-- Data for Name: feedback; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.feedback (id, user_id, user_email, content, list_id, creator_id) FROM stdin;
1	1	testuser1@testuser1.com	Just checking	\N	\N
2	\N	jevine@jevine.com	just checking	\N	\N
3	1	testuser1@testuser1.com	This is awful!	4	2
4	\N	jevine@jevine.com	Testing moved support button	\N	\N
5	6	testuser3@testuser3.com	styling	\N	\N
6	6	testuser3@testuser3.com	Testing forms.py	\N	\N
7	3	admin1@admin1.com	Nah	4	2
8	3	admin1@admin1.com	modal style check	4	2
9	1	testuser1@testuser1.com	yadda yadda	1	3
10	1	testuser1@testuser1.com	blah	4	2
11	3	admin1@admin1.com	blah	4	2
12	3	admin1@admin1.com	blah	4	2
13	3	admin1@admin1.com	Another test.	\N	\N
14	3	admin1@admin1.com	Testing .env	\N	\N
15	3	admin1@admin1.com	Testing.env with report	4	2
\.


--
-- Data for Name: field_data; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.field_data (id, field_id, image_id, value) FROM stdin;
1	4	5	
3	4	14	Spotted
4	7	14	
5	9	14	
6	4	25	
7	7	25	
8	9	25	
\.


--
-- Data for Name: fields; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.fields (id, name, type, list_id) FROM stdin;
4	Color	text	3
5	Color	text	7
7	Description	text	3
9	Got it	text	3
\.


--
-- Data for Name: image; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.image (image_id, list_id, image_url, name) FROM stdin;
1	1	https://farm6.staticflickr.com/5530/13785673395_285d044b65.jpg	P-1 Hawk
2	1	https://farm4.staticflickr.com/3157/4562140266_fb2d52f17f.jpg	P-2 Hawk
3	2	https://farm66.staticflickr.com/65535/53193912641_3a1cdb01da.jpg	Excavator
4	2	https://farm66.staticflickr.com/65535/53100752888_ee04696220.jpg	Dozer (or Bulldozer)
6	4	https://farm66.staticflickr.com/65535/52944894166_46898891be.jpg	Florentine Mosaic
7	1	https://farm66.staticflickr.com/65535/53216898527_e67b97fbab.jpg	P-38 Lightning
8	3	https://farm66.staticflickr.com/65535/53221785607_7085680cbe.jpg	Giraffe
9	5	https://farm66.staticflickr.com/65535/53140023259_bc0716028c.jpg	psychadelic
10	6	https://farm66.staticflickr.com/65535/53103556822_09e5b0f20c.jpg	dude
11	1	https://farm66.staticflickr.com/65535/53225647533_910ef536b6.jpg	Not a plane
13	4	https://farm66.staticflickr.com/65535/53223948614_4d6e08ff74.jpg	asdf
14	3	https://farm66.staticflickr.com/65535/53227839793_7733574916.jpg	asdf
16	7	https://farm66.staticflickr.com/65535/53195688821_6ea8c0a455.jpg	bubble
17	7	https://farm66.staticflickr.com/65535/52001441827_04f0d84c62.jpg	Bubbles Chew
18	7	https://farm66.staticflickr.com/65535/51367862618_bef1e50f38.jpg	BLC
19	9	https://farm66.staticflickr.com/65535/53232226929_daaf1b5848.jpg	asdf
20	13	https://farm66.staticflickr.com/65535/53232837744_1456791a9f.jpg	asdf
21	14	https://farm66.staticflickr.com/65535/53233405165_7b1fb66b7b.jpg	SDFADSFADSF
23	16	https://farm66.staticflickr.com/65535/53231724657_3bc0fb5ee1.jpg	asdf
24	17	https://farm66.staticflickr.com/65535/53233405769_ff82e70833.jpg	asdf
5	3	https://farm66.staticflickr.com/65535/53200619296_91500606db.jpg	Pumaz
26	3	https://live.staticflickr.com/5596/14307815484_87d075481a_b.jpg	Elephant
27	19	https://farm66.staticflickr.com/65535/53233474959_7e623cffe4.jpg	Shuttle
28	3	https://farm66.staticflickr.com/65535/53234895679_dfd04dcf73.jpg	Whoa
29	20	https://farm66.staticflickr.com/65535/53220219936_862380b80a.jpg	Acela
30	20	https://farm66.staticflickr.com/65535/53232781046_bebb168286.jpg	Bullet Train
31	20	https://farm66.staticflickr.com/65535/52258444751_16e0efa941.jpg	Maglev Train
32	20	https://farm66.staticflickr.com/65535/53177109970_f70526a873.jpg	Red Diesel Engine
33	22	https://farm66.staticflickr.com/65535/53235100859_7ee3dbb696.jpg	Octopus
34	17	https://farm66.staticflickr.com/65535/53234774212_2343c726c0.jpg	asdf
35	23	https://farm66.staticflickr.com/65535/52763497160_ffbefca950.jpg	Santa Claus Train
36	16	https://farm66.staticflickr.com/65535/53237135440_d68fc9a998.jpg	asdf
37	29	https://farm66.staticflickr.com/65535/53232307510_245efd7b6f.jpg	Scoot Scoot
25	3	https://live.staticflickr.com/7065/6854959630_8bd5693aa7_b.jpg	leopard
38	36	https://live.staticflickr.com/65535/53237043987_2b950f161a_m.jpg	a
39	36	https://live.staticflickr.com/65535/53238471170_5b3e2a68c7_m.jpg	about
40	36	https://live.staticflickr.com/65535/53237133202_88cb9e1d7a_m.jpg	all
42	21	https://farm66.staticflickr.com/65535/53238118506_8984c9846f.jpg	test
44	21	https://farm66.staticflickr.com/65535/53238609815_cc0f05f280.jpg	test
43	21	https://farm66.staticflickr.com/65535/53238609815_cc0f05f280.jpg	test
45	21	https://live.staticflickr.com/65535/53219751786_4837bdff77_h.jpg	test
46	21	https://farm66.staticflickr.com/65535/53238684914_fc8309c420.jpg	test
47	21	https://live.staticflickr.com/65535/53219751786_4837bdff77_h.jpg	test
\.


--
-- Data for Name: image_list; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.image_list (list_id, name, description, creator_id, category_id, core_list) FROM stdin;
1	American WWII Fighters	Images of WWII fighter planes flown by the United States Air Force.	3	2	t
2	Construction Vehicles	Various types of construction vehicles.	3	2	f
4	Jigsaw Puzzles	My list of owned jigsaw puzzles.	2	\N	f
5	Test 1 no core	\N	3	3	f
6	Test 2 core	\N	3	3	t
7	Bubble Gummers	\N	6	\N	f
13	Onemoretime2	\N	3	5	t
14	test 1 no core test 1 no core test 1 no core 	\N	3	1	f
16	More giraffes	\N	3	\N	f
19	Another List	\N	1	\N	f
3	Zooniebabas	Various animals you might find in a zoo.	1	\N	f
20	Trains for Sebastien	\N	1	\N	f
21	MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM	\N	3	\N	f
22	Sea Creatures	\N	3	\N	f
23	Hohoho	\N	3	7	t
17	Boogedy2	\N	3	\N	t
29	Scooters	\N	1	2	f
9	coretest	\N	3	\N	t
30	Pre-K Word List (Dolch)	\N	3	8	t
31	Kindergarten Word List (Dolch)	\N	3	8	t
32	First Grade Word List (Dolch)	\N	3	8	t
33	Second Grade Word List (Dolch)	\N	3	8	f
34	Third Grade Word List (Dolch)	\N	3	8	t
35	Noun Dolch Word List (Dolch)	\N	3	8	t
36	1st 100 Fry Sight Words	\N	3	9	t
\.


--
-- Data for Name: image_position; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.image_position (id, image_id, list_id, "position") FROM stdin;
3	3	2	1
4	4	2	2
6	6	4	1
16	16	7	3
17	17	7	1
18	18	7	2
19	19	9	1
20	20	13	1
21	21	14	1
37	37	29	1
24	24	17	1
27	27	19	1
5	5	3	4
8	8	3	2
14	14	3	3
25	25	3	1
9	9	5	1
10	10	6	1
26	26	3	5
28	28	3	6
38	38	36	1
39	39	36	2
40	40	36	3
42	42	21	1
43	43	21	2
44	44	21	3
45	45	21	4
46	46	21	5
47	47	21	6
13	13	4	2
29	29	20	1
30	30	20	2
31	31	20	3
32	32	20	4
33	33	22	1
1	1	1	3
2	2	1	4
7	7	1	2
11	11	1	1
34	34	17	2
35	35	23	1
23	23	16	1
36	36	16	2
\.


--
-- Data for Name: list_category; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.list_category (category_id, name, description) FROM stdin;
1	Animals	\N
2	Vehicles	\N
3	Groovy	\N
4	Onemoretime	\N
5	Onemoretime2	\N
7	Christmas	\N
8	Dolch sight words lists	\N
9	Fry sight words lists	\N
\.


--
-- Data for Name: user_image; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.user_image (user_image_id, user_id, image_id, name, description, is_custom_added) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: kodai
--

COPY public.users (id, username, password_hash, email, is_admin, first_name, last_name) FROM stdin;
2	testuser2	$2b$12$A3KkoUmXugFAgMdOdR96keNoyPBMwzET8Z5SpS5LLWHJEi6DqTDSy	testuser2@testuser2.com	f	Testy2	User2
3	admin1	$2b$12$RrZk62JfWZGelxB7fLtJAe2UuYbluMwmIG2uOsghE9TgqX6IdhFeu	admin1@admin1.com	t	admin1	admin1
4	admin2	$2b$12$OlCIIJZQJvfsonHB5b9M2e58Vv1Bvadej63e6PIXuVGCAGKVI0P5u	admin2@admin2.com	t	admin2	admin2
1	testuser1	$2b$12$TNPD4bwFeksaKfO9MxrwPuLZXU81XPOsWOMn4teCclGQvLWUKSc/C	testuser1@testuser1.com	f	testuser1	testuser1
6	testuser3	$2b$12$IhEb.L/543pnPYOjArBZDeNG2aXKxqj3ekkCsobWRhtnhin5uNtte	testuser3@testuser3.com	f	testuser3	testuser3
\.


--
-- Name: feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.feedback_id_seq', 15, true);


--
-- Name: field_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.field_data_id_seq', 8, true);


--
-- Name: fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.fields_id_seq', 9, true);


--
-- Name: image_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.image_image_id_seq', 47, true);


--
-- Name: image_list_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.image_list_list_id_seq', 36, true);


--
-- Name: image_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.image_position_id_seq', 47, true);


--
-- Name: list_category_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.list_category_category_id_seq', 9, true);


--
-- Name: user_image_user_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.user_image_user_image_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kodai
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);


--
-- Name: field_data field_data_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.field_data
    ADD CONSTRAINT field_data_pkey PRIMARY KEY (id);


--
-- Name: fields fields_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_pkey PRIMARY KEY (id);


--
-- Name: image_list image_list_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image_list
    ADD CONSTRAINT image_list_pkey PRIMARY KEY (list_id);


--
-- Name: image image_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image
    ADD CONSTRAINT image_pkey PRIMARY KEY (image_id);


--
-- Name: image_position image_position_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image_position
    ADD CONSTRAINT image_position_pkey PRIMARY KEY (id);


--
-- Name: list_category list_category_name_key; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.list_category
    ADD CONSTRAINT list_category_name_key UNIQUE (name);


--
-- Name: list_category list_category_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.list_category
    ADD CONSTRAINT list_category_pkey PRIMARY KEY (category_id);


--
-- Name: user_image user_image_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.user_image
    ADD CONSTRAINT user_image_pkey PRIMARY KEY (user_image_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: feedback feedback_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- Name: feedback feedback_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.image_list(list_id);


--
-- Name: feedback feedback_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: field_data field_data_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.field_data
    ADD CONSTRAINT field_data_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id) ON DELETE CASCADE;


--
-- Name: field_data field_data_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.field_data
    ADD CONSTRAINT field_data_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.image(image_id) ON DELETE CASCADE;


--
-- Name: fields fields_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.image_list(list_id) ON DELETE CASCADE;


--
-- Name: image_list image_list_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image_list
    ADD CONSTRAINT image_list_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.list_category(category_id) ON DELETE SET NULL;


--
-- Name: image_list image_list_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image_list
    ADD CONSTRAINT image_list_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- Name: image image_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image
    ADD CONSTRAINT image_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.image_list(list_id);


--
-- Name: image_position image_position_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image_position
    ADD CONSTRAINT image_position_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.image(image_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: image_position image_position_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.image_position
    ADD CONSTRAINT image_position_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.image_list(list_id) ON DELETE CASCADE;


--
-- Name: user_image user_image_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.user_image
    ADD CONSTRAINT user_image_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.image(image_id);


--
-- Name: user_image user_image_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kodai
--

ALTER TABLE ONLY public.user_image
    ADD CONSTRAINT user_image_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

