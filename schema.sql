--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Debian 16.8-1.pgdg120+1)
-- Dumped by pg_dump version 16.8 (Debian 16.8-1.pgdg120+1)

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

--
-- Name: check_alert_trigger(); Type: FUNCTION; Schema: public; Owner: testuser
--

CREATE FUNCTION public.check_alert_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
	alert_row RECORD;
	measure_value FLOAT;
BEGIN
	measure_value := NEW.value::FLOAT;

	FOR alert_row IN
		SELECT ta.id, ta.value, ta.math_signal
		FROM type_alerts ta
		WHERE ta.parameter_id = NEW.parameter_id AND ta.is_active
	LOOP
		IF (
			(alert_row.math_signal = '>' AND measure_value > alert_row.value) OR
			(alert_row.math_signal = '<' AND measure_value < alert_row.value) OR
			(alert_row.math_signal = '=' AND measure_value = alert_row.value)
		) THEN
			INSERT INTO alerts (measure_id, type_alert_id, create_date, is_read)
			VALUES (NEW.id, alert_row.id, EXTRACT(EPOCH FROM NOW())::INT, FALSE);
		END IF;
	END LOOP;

	RETURN NEW;
END;
$$;


ALTER FUNCTION public.check_alert_trigger() OWNER TO testuser;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO testuser;

--
-- Name: alerts; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.alerts (
    id bigint NOT NULL,
    measure_id bigint NOT NULL,
    type_alert_id bigint NOT NULL,
    create_date integer DEFAULT EXTRACT(epoch FROM now()) NOT NULL,
    is_read boolean DEFAULT false NOT NULL
);


ALTER TABLE public.alerts OWNER TO testuser;

--
-- Name: alerts_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.alerts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.alerts_id_seq OWNER TO testuser;

--
-- Name: alerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.alerts_id_seq OWNED BY public.alerts.id;


--
-- Name: measures; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.measures (
    id bigint NOT NULL,
    value double precision NOT NULL,
    measure_date integer DEFAULT EXTRACT(epoch FROM now()) NOT NULL,
    parameter_id bigint NOT NULL
);


ALTER TABLE public.measures OWNER TO testuser;

--
-- Name: measures_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.measures_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.measures_id_seq OWNER TO testuser;

--
-- Name: measures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.measures_id_seq OWNED BY public.measures.id;


--
-- Name: parameter_types; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.parameter_types (
    id bigint NOT NULL,
    name character varying NOT NULL,
    detect_type character varying,
    measure_unit character varying NOT NULL,
    qnt_decimals integer NOT NULL,
    "offset" double precision,
    factor double precision,
    create_date integer DEFAULT EXTRACT(epoch FROM now()) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.parameter_types OWNER TO testuser;

--
-- Name: parameter_types_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.parameter_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parameter_types_id_seq OWNER TO testuser;

--
-- Name: parameter_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.parameter_types_id_seq OWNED BY public.parameter_types.id;


--
-- Name: parameters; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.parameters (
    id bigint NOT NULL,
    parameter_type_id bigint NOT NULL,
    station_id bigint NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.parameters OWNER TO testuser;

--
-- Name: parameters_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.parameters_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parameters_id_seq OWNER TO testuser;

--
-- Name: parameters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.parameters_id_seq OWNED BY public.parameters.id;


--
-- Name: type_alerts; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.type_alerts (
    id bigint NOT NULL,
    parameter_id bigint,
    name character varying NOT NULL,
    value integer NOT NULL,
    math_signal character varying NOT NULL,
    create_date integer DEFAULT EXTRACT(epoch FROM now()) NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL,
    status character varying DEFAULT 'D'::character varying NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.type_alerts OWNER TO testuser;

--
-- Name: type_alerts_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.type_alerts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.type_alerts_id_seq OWNER TO testuser;

--
-- Name: type_alerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.type_alerts_id_seq OWNED BY public.type_alerts.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    create_date timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL,
    old_password json DEFAULT '[]'::jsonb NOT NULL
);


ALTER TABLE public.users OWNER TO testuser;

--
-- Name: COLUMN users.old_password; Type: COMMENT; Schema: public; Owner: testuser
--

COMMENT ON COLUMN public.users.old_password IS 'List of old passwords';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: codenine
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO testuser;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: weather_stations; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.weather_stations (
    id bigint NOT NULL,
    name character varying NOT NULL,
    uid character varying NOT NULL,
    address json DEFAULT '[]'::jsonb NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    create_date integer DEFAULT EXTRACT(epoch FROM now()) NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.weather_stations OWNER TO testuser;

--
-- Name: COLUMN weather_stations.address; Type: COMMENT; Schema: public; Owner: testuser
--

COMMENT ON COLUMN public.weather_stations.address IS 'List of address';


--
-- Name: weather_stations_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.weather_stations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weather_stations_id_seq OWNER TO testuser;

--
-- Name: weather_stations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.weather_stations_id_seq OWNED BY public.weather_stations.id;


--
-- Name: alerts id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.alerts ALTER COLUMN id SET DEFAULT nextval('public.alerts_id_seq'::regclass);


--
-- Name: measures id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.measures ALTER COLUMN id SET DEFAULT nextval('public.measures_id_seq'::regclass);


--
-- Name: parameter_types id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.parameter_types ALTER COLUMN id SET DEFAULT nextval('public.parameter_types_id_seq'::regclass);


--
-- Name: parameters id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.parameters ALTER COLUMN id SET DEFAULT nextval('public.parameters_id_seq'::regclass);


--
-- Name: type_alerts id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.type_alerts ALTER COLUMN id SET DEFAULT nextval('public.type_alerts_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: weather_stations id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.weather_stations ALTER COLUMN id SET DEFAULT nextval('public.weather_stations_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: alerts alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_pkey PRIMARY KEY (id);


--
-- Name: measures measures_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.measures
    ADD CONSTRAINT measures_pkey PRIMARY KEY (id);


--
-- Name: parameter_types parameter_types_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.parameter_types
    ADD CONSTRAINT parameter_types_pkey PRIMARY KEY (id);


--
-- Name: parameters parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.parameters
    ADD CONSTRAINT parameters_pkey PRIMARY KEY (id);


--
-- Name: type_alerts type_alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.type_alerts
    ADD CONSTRAINT type_alerts_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: weather_stations weather_stations_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.weather_stations
    ADD CONSTRAINT weather_stations_pkey PRIMARY KEY (id);


--
-- Name: weather_stations weather_stations_uid_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.weather_stations
    ADD CONSTRAINT weather_stations_uid_key UNIQUE (uid);


--
-- Name: ix_alerts_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_alerts_id ON public.alerts USING btree (id);


--
-- Name: ix_alerts_measure_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_alerts_measure_id ON public.alerts USING btree (measure_id);


--
-- Name: ix_alerts_type_alert_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_alerts_type_alert_id ON public.alerts USING btree (type_alert_id);


--
-- Name: ix_measures_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_measures_id ON public.measures USING btree (id);


--
-- Name: ix_measures_parameter_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_measures_parameter_id ON public.measures USING btree (parameter_id);


--
-- Name: ix_parameter_types_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_parameter_types_id ON public.parameter_types USING btree (id);


--
-- Name: ix_parameters_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_parameters_id ON public.parameters USING btree (id);


--
-- Name: ix_parameters_parameter_type_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_parameters_parameter_type_id ON public.parameters USING btree (parameter_type_id);


--
-- Name: ix_parameters_station_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_parameters_station_id ON public.parameters USING btree (station_id);


--
-- Name: ix_type_alerts_create_date; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_type_alerts_create_date ON public.type_alerts USING btree (create_date);


--
-- Name: ix_type_alerts_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_type_alerts_id ON public.type_alerts USING btree (id);


--
-- Name: ix_type_alerts_parameter_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_type_alerts_parameter_id ON public.type_alerts USING btree (parameter_id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_weather_stations_id; Type: INDEX; Schema: public; Owner: testuser
--

CREATE INDEX ix_weather_stations_id ON public.weather_stations USING btree (id);


--
-- Name: alerts alerts_measure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_measure_id_fkey FOREIGN KEY (measure_id) REFERENCES public.measures(id);


--
-- Name: alerts alerts_type_alert_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_type_alert_id_fkey FOREIGN KEY (type_alert_id) REFERENCES public.type_alerts(id);


--
-- Name: measures measures_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.measures
    ADD CONSTRAINT measures_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES public.parameters(id);


--
-- Name: parameters parameters_parameter_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.parameters
    ADD CONSTRAINT parameters_parameter_type_id_fkey FOREIGN KEY (parameter_type_id) REFERENCES public.parameter_types(id);


--
-- Name: parameters parameters_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.parameters
    ADD CONSTRAINT parameters_station_id_fkey FOREIGN KEY (station_id) REFERENCES public.weather_stations(id);


--
-- Name: type_alerts type_alerts_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.type_alerts
    ADD CONSTRAINT type_alerts_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES public.parameters(id);


--
-- PostgreSQL database dump complete
--