create table t_likes(message_id varchar(255) NOT NULL, user_id varchar(255) NOT NULL ,
     choice_value varchar(255), CONSTRAINT PK_LIKES PRIMARY KEY (message_id,user_id));

