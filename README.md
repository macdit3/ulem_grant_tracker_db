# Ulem Grant Tracker Database System

## Overview
The ULEM Grants Tracker Database System is a comprehensive solution for managing incoming grants, donors, 
donations, pledges, tax_receipts, and thank you notes. Users are able to track and manage all aspects of 
the grant process, starting from generating instance reports, to sending thank you notes and tax receipt to donors.

## Features
- User-friendly interface for booking concert tickets.
- Real-time ticket availability updates.
- Secure and efficient ticket reservation process.
- Modular design for easy maintenance and scalability.

## Prerequisites
- Python 3.8 or higher
- Required libraries (listed in `requirements.txt`)

## Installation
1. Clone the repository:
    ```bash
    git clone git@github.com:macdit3/ulem_grant_tracker_db.git
    ```
2. Navigate to the project directory:
    ```bash
    cd ulem_grant_tracker_db
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the script using the following command:
```bash
python main.py
```

Follow the on-screen instructions to book tickets or manage the system.

## File Structure
- `main.py`: Entry point of the application.
- `requirements.txt`: List of dependencies.
- Other supporting modules and files.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or support, please contact macueidit@gmail.com.


### Assigned problem statement:
-- Give all donors who have donated $ 500+ but we haven't sent a thank you note yet
-- TODO your task is to solve the problem above using "LEFT JOIN"
SELECT
    -- all columns
        dn.first_name,
        dn.last_name,
        dn.donor_type,
        dt.amount,
        pg.description,
        tyn.notes,
        tyn.sent_date

FROM donors dn
-- INNER JOIN
         inner join donations dt on dn.id = dt.donor_id
         inner join public.programs pg on pg.id = dt.program_id
         left join public.thank_you_notes tyn on dn.id = tyn.donor_id

WHERE dn.first_name IS NOT NULL
ORDER BY dt.amount DESC
LIMIT 10




### Prompt for generating mock data for my database testing:

Based on the provided DDL sql script, can you generate real-to-life 
mock data or sample data for my 6 table limiting 5 records or rows per table.
U
Do not write the response or output code on notebook use raw SQL file.

the DDL of my database table is below:
create table public.donors
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


create table public.programs
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

create table public.donations
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

create table public.pledges
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

create table public.tax_receipts
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

create table public.thank_you_notes
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

