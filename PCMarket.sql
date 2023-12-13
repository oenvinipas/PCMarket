CREATE DATABASE pcmarket;

create table users
(
    user_id serial primary key,
    email varchar(255) not null unique,
    password varchar(255) not null,
    first_name varchar(255) not null,
    last_name varchar(255)
);

create table computer
(
    computer_id serial primary key,
    name varchar(255) default 'computer',
    description varchar(255) default '-',
    image varchar(255),
    price varchar(255) not null,
    "case" varchar(255) default '-',
    motherboard varchar(255) default '-',
    cpu varchar(255) default '-',
    gpu varchar(255) default '-',
    ram varchar(255) default '-',
    memory varchar(255) default '-',
    fans varchar(255) default '-',
    power_supply varchar(255) default '-',
    condition varchar(255) default '-',
    rgb bool default false
);

create table posts
(
    post_id serial primary key,
    user_id integer references users(user_id),
    computer_id integer references computer(computer_id),
    top_bidder integer references users(user_id),
    bid_count integer default 0,
    bid_days integer not null
);

create table comments
(
    comment_id serial primary key ,
    post_id integer references posts(post_id),
    user_id integer references users(user_id),
    comment varchar(255)
);