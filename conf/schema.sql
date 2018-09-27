--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5
-- Dumped by pg_dump version 10.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: egfds; Type: SCHEMA; Schema: -; Owner: root
--

CREATE SCHEMA egfds;


ALTER SCHEMA egfds OWNER TO root;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: comment; Type: TABLE; Schema: egfds; Owner: root
--

CREATE TABLE egfds.comment (
    id bigint NOT NULL,
    vote_id bigint NOT NULL,
    comment text,
    promoted boolean DEFAULT false NOT NULL
);


ALTER TABLE egfds.comment OWNER TO root;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: egfds; Owner: root
--

CREATE SEQUENCE egfds.comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE egfds.comment_id_seq OWNER TO root;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: egfds; Owner: root
--

ALTER SEQUENCE egfds.comment_id_seq OWNED BY egfds.comment.id;


--
-- Name: game; Type: TABLE; Schema: egfds; Owner: root
--

CREATE TABLE egfds.game (
    id bigint NOT NULL,
    name text NOT NULL,
    genre_id bigint NOT NULL
);


ALTER TABLE egfds.game OWNER TO root;

--
-- Name: game_id_seq; Type: SEQUENCE; Schema: egfds; Owner: root
--

CREATE SEQUENCE egfds.game_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE egfds.game_id_seq OWNER TO root;

--
-- Name: game_id_seq; Type: SEQUENCE OWNED BY; Schema: egfds; Owner: root
--

ALTER SEQUENCE egfds.game_id_seq OWNED BY egfds.game.id;


--
-- Name: game_instance; Type: TABLE; Schema: egfds; Owner: root
--

CREATE TABLE egfds.game_instance (
    id bigint NOT NULL,
    game_id bigint NOT NULL,
    platform_id bigint NOT NULL
);


ALTER TABLE egfds.game_instance OWNER TO root;

--
-- Name: game_instance_id_seq; Type: SEQUENCE; Schema: egfds; Owner: root
--

CREATE SEQUENCE egfds.game_instance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE egfds.game_instance_id_seq OWNER TO root;

--
-- Name: game_instance_id_seq; Type: SEQUENCE OWNED BY; Schema: egfds; Owner: root
--

ALTER SEQUENCE egfds.game_instance_id_seq OWNED BY egfds.game_instance.id;


--
-- Name: genre; Type: TABLE; Schema: egfds; Owner: root
--

CREATE TABLE egfds.genre (
    id bigint NOT NULL,
    name text NOT NULL
);


ALTER TABLE egfds.genre OWNER TO root;

--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: egfds; Owner: root
--

CREATE SEQUENCE egfds.genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE egfds.genre_id_seq OWNER TO root;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: egfds; Owner: root
--

ALTER SEQUENCE egfds.genre_id_seq OWNED BY egfds.genre.id;


--
-- Name: platform; Type: TABLE; Schema: egfds; Owner: root
--

CREATE TABLE egfds.platform (
    id bigint NOT NULL,
    name character varying(40) NOT NULL
);


ALTER TABLE egfds.platform OWNER TO root;

--
-- Name: platform_id_seq; Type: SEQUENCE; Schema: egfds; Owner: root
--

CREATE SEQUENCE egfds.platform_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE egfds.platform_id_seq OWNER TO root;

--
-- Name: platform_id_seq; Type: SEQUENCE OWNED BY; Schema: egfds; Owner: root
--

ALTER SEQUENCE egfds.platform_id_seq OWNED BY egfds.platform.id;


--
-- Name: user; Type: TABLE; Schema: egfds; Owner: root
--

CREATE TABLE egfds."user" (
    id bigint NOT NULL,
    username character varying(30) NOT NULL,
    admin boolean DEFAULT false NOT NULL,
    password text,
    deleted boolean DEFAULT false NOT NULL
);


ALTER TABLE egfds."user" OWNER TO root;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: egfds; Owner: root
--

CREATE SEQUENCE egfds.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE egfds.user_id_seq OWNER TO root;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: egfds; Owner: root
--

ALTER SEQUENCE egfds.user_id_seq OWNED BY egfds."user".id;


--
-- Name: vote; Type: TABLE; Schema: egfds; Owner: root
--

CREATE TABLE egfds.vote (
    id bigint NOT NULL,
    vote smallint DEFAULT '0'::smallint NOT NULL,
    user_id bigint NOT NULL,
    instance_id bigint NOT NULL,
    date timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE egfds.vote OWNER TO root;

--
-- Name: vote_id_seq; Type: SEQUENCE; Schema: egfds; Owner: root
--

CREATE SEQUENCE egfds.vote_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE egfds.vote_id_seq OWNER TO root;

--
-- Name: vote_id_seq; Type: SEQUENCE OWNED BY; Schema: egfds; Owner: root
--

ALTER SEQUENCE egfds.vote_id_seq OWNED BY egfds.vote.id;


--
-- Name: comment id; Type: DEFAULT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.comment ALTER COLUMN id SET DEFAULT nextval('egfds.comment_id_seq'::regclass);


--
-- Name: game id; Type: DEFAULT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.game ALTER COLUMN id SET DEFAULT nextval('egfds.game_id_seq'::regclass);


--
-- Name: game_instance id; Type: DEFAULT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.game_instance ALTER COLUMN id SET DEFAULT nextval('egfds.game_instance_id_seq'::regclass);


--
-- Name: genre id; Type: DEFAULT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.genre ALTER COLUMN id SET DEFAULT nextval('egfds.genre_id_seq'::regclass);


--
-- Name: platform id; Type: DEFAULT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.platform ALTER COLUMN id SET DEFAULT nextval('egfds.platform_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds."user" ALTER COLUMN id SET DEFAULT nextval('egfds.user_id_seq'::regclass);


--
-- Name: vote id; Type: DEFAULT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.vote ALTER COLUMN id SET DEFAULT nextval('egfds.vote_id_seq'::regclass);


--
-- Name: comment idx_16507_primary; Type: CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.comment
    ADD CONSTRAINT idx_16507_primary PRIMARY KEY (id);


--
-- Name: game idx_16517_primary; Type: CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.game
    ADD CONSTRAINT idx_16517_primary PRIMARY KEY (id);


--
-- Name: game_instance idx_16526_primary; Type: CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.game_instance
    ADD CONSTRAINT idx_16526_primary PRIMARY KEY (id);


--
-- Name: genre idx_16532_primary; Type: CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.genre
    ADD CONSTRAINT idx_16532_primary PRIMARY KEY (id);


--
-- Name: platform idx_16541_primary; Type: CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.platform
    ADD CONSTRAINT idx_16541_primary PRIMARY KEY (id);


--
-- Name: user idx_16547_primary; Type: CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds."user"
    ADD CONSTRAINT idx_16547_primary PRIMARY KEY (id);


--
-- Name: vote idx_16558_primary; Type: CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.vote
    ADD CONSTRAINT idx_16558_primary PRIMARY KEY (id);


--
-- Name: idx_16507_vote_id; Type: INDEX; Schema: egfds; Owner: root
--

CREATE INDEX idx_16507_vote_id ON egfds.comment USING btree (vote_id);


--
-- Name: idx_16517_genre_id; Type: INDEX; Schema: egfds; Owner: root
--

CREATE INDEX idx_16517_genre_id ON egfds.game USING btree (genre_id);


--
-- Name: idx_16526_game_id; Type: INDEX; Schema: egfds; Owner: root
--

CREATE UNIQUE INDEX idx_16526_game_id ON egfds.game_instance USING btree (game_id, platform_id);


--
-- Name: idx_16526_platform_id; Type: INDEX; Schema: egfds; Owner: root
--

CREATE INDEX idx_16526_platform_id ON egfds.game_instance USING btree (platform_id);


--
-- Name: idx_16541_name; Type: INDEX; Schema: egfds; Owner: root
--

CREATE UNIQUE INDEX idx_16541_name ON egfds.platform USING btree (name);


--
-- Name: idx_16547_username; Type: INDEX; Schema: egfds; Owner: root
--

CREATE UNIQUE INDEX idx_16547_username ON egfds."user" USING btree (username);


--
-- Name: idx_16558_instance_id; Type: INDEX; Schema: egfds; Owner: root
--

CREATE INDEX idx_16558_instance_id ON egfds.vote USING btree (instance_id);


--
-- Name: idx_16558_vote_ibfk_1; Type: INDEX; Schema: egfds; Owner: root
--

CREATE INDEX idx_16558_vote_ibfk_1 ON egfds.vote USING btree (instance_id);


--
-- Name: idx_16558_vote_per_user; Type: INDEX; Schema: egfds; Owner: root
--

CREATE UNIQUE INDEX idx_16558_vote_per_user ON egfds.vote USING btree (user_id, instance_id);


--
-- Name: comment comment_ibfk_1; Type: FK CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.comment
    ADD CONSTRAINT comment_ibfk_1 FOREIGN KEY (vote_id) REFERENCES egfds.vote(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: game game_ibfk_1; Type: FK CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.game
    ADD CONSTRAINT game_ibfk_1 FOREIGN KEY (genre_id) REFERENCES egfds.genre(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: game_instance game_instance_ibfk_1; Type: FK CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.game_instance
    ADD CONSTRAINT game_instance_ibfk_1 FOREIGN KEY (game_id) REFERENCES egfds.game(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: game_instance game_instance_ibfk_2; Type: FK CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.game_instance
    ADD CONSTRAINT game_instance_ibfk_2 FOREIGN KEY (platform_id) REFERENCES egfds.platform(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: vote vote_ibfk_1; Type: FK CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.vote
    ADD CONSTRAINT vote_ibfk_1 FOREIGN KEY (instance_id) REFERENCES egfds.game_instance(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: vote vote_ibfk_2; Type: FK CONSTRAINT; Schema: egfds; Owner: root
--

ALTER TABLE ONLY egfds.vote
    ADD CONSTRAINT vote_ibfk_2 FOREIGN KEY (user_id) REFERENCES egfds."user"(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

