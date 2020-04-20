DROP SCHEMA IF EXISTS public CASCADE;

CREATE SCHEMA public;
SET search_path TO public;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS test_table
(
 column_1 character varying(255) PRIMARY KEY NOT NULL,
 column_2 character varying(255) NOT NULL,
 column_3 character varying(255) NOT NULL
);