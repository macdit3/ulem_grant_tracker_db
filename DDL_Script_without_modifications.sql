create table if not exists public.donors
(
    id                       serial
        primary key,
    donor_type               varchar(20) not null,
    first_name               varchar(100),
    last_name                varchar(100),
    organization_name        varchar(200),
    email                    varchar(255),
    phone                    varchar(20),
    address_line1            varchar(255),
    address_line2            varchar(255),
    city                     varchar(100),
    state                    varchar(100),
    postal_code              varchar(20),
    country                  varchar(100),
    preferred_contact_method varchar(20),
    notes                    text,
    created_at               timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at               timestamp with time zone default CURRENT_TIMESTAMP
);

alter table public.donors
    owner to admin;

create table if not exists public.programs
(
    id               serial
        primary key,
    name             varchar(200) not null,
    description      text,
    start_date       date,
    end_date         date,
    budget           numeric(10, 2),
    goal_amount      numeric(10, 2),
    current_progress numeric(10, 2),
    created_at       timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at       timestamp with time zone default CURRENT_TIMESTAMP
);

alter table public.programs
    owner to admin;

create table if not exists public.donations
(
    id                serial
        primary key,
    donor_id          integer
        references public.donors,
    program_id        integer
        references public.programs,
    amount            numeric(10, 2) not null,
    donation_date     date           not null,
    payment_method    varchar(50),
    transaction_id    varchar(100),
    is_tax_deductible boolean                  default false,
    notes             text,
    created_at        timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at        timestamp with time zone default CURRENT_TIMESTAMP
);

alter table public.donations
    owner to admin;

create table if not exists public.pledges
(
    id               serial
        primary key,
    donor_id         integer
        references public.donors,
    program_id       integer
        references public.programs,
    amount           numeric(10, 2) not null,
    pledge_date      date           not null,
    fulfillment_date date,
    status           varchar(50),
    amount_fulfilled numeric(10, 2) not null,
    notes            text,
    created_at       timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at       timestamp with time zone default CURRENT_TIMESTAMP
);

alter table public.pledges
    owner to admin;

create table if not exists public.tax_receipts
(
    id             serial
        primary key,
    donor_id       integer
        references public.donations,
    year_donated   date,
    total_amount   numeric(10, 2) not null,
    generated_date date           not null,
    sent_date      date,
    created_at     timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at     timestamp with time zone default CURRENT_TIMESTAMP
);

alter table public.tax_receipts
    owner to admin;

create table if not exists public.thank_you_notes
(
    id            serial
        primary key,
    donor_id      integer
        references public.donors,
    donation_id   integer
        references public.donations,
    sent_date     date,
    method        varchar(50),
    template_used varchar(100),
    notes         text,
    created_at    timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at    timestamp with time zone default CURRENT_TIMESTAMP
);

alter table public.thank_you_notes
    owner to admin;

