create table game_db;
use game_db;
create table player
(
    id int AUTO_INCREMENT primary key,
    username varchar(255) not null unique,
    pasword varchar(255) not null
);
create table result
(
    id int AUTO_INCREMENT primary key,
    player_id int,
    player_score int,
    dealer_score int,
    result varchar(10),
    timestamp datetime
    foreign key (player_id)references player(id)
);