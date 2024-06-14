SET GLOBAL local_infile = 1;

CREATE TABLE IF NOT EXISTS job
(
    id                        int       NOT  NULL
        PRIMARY KEY,
    created_by                text      ,
    created_date              timestamp ,
    last_modified_by          text      ,
    last_modified_date        timestamp ,
    is_active                 int       ,
    title                     text      ,
    description               text      ,
    work_schedule             text      ,
    radius_unit               text      ,
    location_state            timestamp ,
    location_list             text      ,
    role_location             text      ,
    resume_option             text      ,
    budget                    int       ,
    status                    int       ,
    error                     text      ,
    template_question_id      int       ,
    template_question_name    text      ,
    question_form_description text      ,
    redirect_url              text      ,
    start_date                timestamp ,
    end_date                  timestamp ,
    close_date                timestamp ,
    group_id                  int       ,
    minor_id                  int       ,
    campaign_id               int       ,
    company_id                int       ,
    history_status            int       ,
    CONSTRAINT id
        UNIQUE (id)
);


LOAD DATA LOCAL INFILE '/var/lib/mysql-files/MySQL/job.csv'
INTO TABLE job
FIELDS TERMINATED BY ','
IGNORE 1 LINES;



CREATE TABLE IF NOT EXISTS master_publisher
(
id                        int       NOT    NULL
        PRIMARY KEY,
    created_by                text       ,
    created_date              timestamp  ,
    last_modified_by          text       ,
    last_modified_date        timestamp  ,
    is_active                 int        ,
    title                     text       ,
    description               text       ,
    work_schedule             text       ,
    radius_unit               text       ,
    location_state            timestamp  ,
    location_list             text       ,
    role_location             text       ,
    resume_option             text       ,
    budget                    int        ,
    status                    int        ,
    error                     text       ,
    template_question_id      int        ,
    template_question_name    text       ,
    question_form_description text       ,
    redirect_url              text       ,
    start_date                timestamp  ,
    end_date                  timestamp  ,
    close_date                timestamp  ,
    group_id                  int        ,
    minor_id                  int        ,
    campaign_id               int        ,
    company_id                int        ,
    history_status            int        ,
    CONSTRAINT id
        UNIQUE (id)
);

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/MySQL/master_publisher.csv'
INTO TABLE master_publisher
FIELDS TERMINATED BY ','
IGNORE 1 LINES;


CREATE TABLE IF NOT EXISTS company
(
    id                  int       NOT   NULL
        PRIMARY KEY,
    created_by          text        ,
    created_date        timestamp   ,
    last_modified_by    text        ,
    last_modified_date  timestamp   ,
    is_active           int         ,
    name                text        ,
    is_agree_conditon   int         ,
    is_agree_sign_deal  int         ,
    sign_deal_user      text        ,
    billing_id          int         ,
    manage_type         int         ,
    customer_type       int         ,
    status              int         ,
    publisher_id        int         ,
    flat_rate           text        ,
    percentage_of_click text        ,
    logo                text        ,
    CONSTRAINT id
        UNIQUE (id)
);

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/MySQL/company.csv'
INTO TABLE company
FIELDS TERMINATED BY ','
IGNORE 1 LINES;


CREATE TABLE IF NOT EXISTS `group`
(
    id                 int       NOT NULL
        PRIMARY KEY,
    created_by         text      ,
    created_date       timestamp ,
    last_modified_by   text      ,
    last_modified_date timestamp ,
    is_active          int       ,
    name               text      ,
    budget_group       int       ,
    status             int       ,
    company_id         int       ,
    campaign_id        int       ,
    number_of_pacing   int       ,
    CONSTRAINT id
        UNIQUE (id)
);

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/MySQL/group.csv'
INTO TABLE `group`
FIELDS TERMINATED BY ','
IGNORE 1 LINES;


CREATE TABLE IF NOT EXISTS company
(
    id                  int       NOT NULL
        PRIMARY KEY,
    created_by          text      ,
    created_date        timestamp ,
    last_modified_by    text      ,
    last_modified_date  timestamp ,
    is_active           int       ,
    name                text      ,
    is_agree_conditon   int       ,
    is_agree_sign_deal  int       ,
    sign_deal_user      text      ,
    billing_id          int       ,
    manage_type         int       ,
    customer_type       int       ,
    status              int       ,
    publisher_id        int       ,
    flat_rate           text      ,
    percentage_of_click text      ,
    logo                text      ,
    CONSTRAINT id
        UNIQUE (id)
);

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/MySQL/company.csv'
INTO TABLE company
FIELDS TERMINATED BY ','
IGNORE 1 LINES;

