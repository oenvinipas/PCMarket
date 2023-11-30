CREATE DATABASE pcmarket;

CREATE TABLE users
(
    user_id serial primary key,
    email varchar(255) not null unique,
    password varchar(255) not null,
    first_name varchar(255) not null,
    last_name varchar(255)
);

CREATE TABLE computer
(
    computer_id serial primary key,
    description varchar(255) default '-',
    image varchar(255),
    "case" varchar(255) default '-',
    cpu varchar(255) default '-',
    gpu varchar(255) default '-',
    ram varchar(255) default '-',
    memory varchar(255) default '-',
    fans varchar(255) default '-',
    power_supply varchar(255) default '-',
    condition varchar(255) default '-',
    rgb bool default false
);

CREATE TABLE posts
(
    post_id serial primary key,
    user_id integer references users(user_id),
    computer_id integer references computer(computer_id)
);

CREATE TABLE comments
(
    comment_id serial,
    post_id integer references posts(post_id),
    user_id integer references users(user_id),
    primary key (comment_id)
);