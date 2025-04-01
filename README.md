## Ulem Grant Tracker Database

This is a simple database that stores grant information in a list of dictionaries. 
Each dictionary represents a single grant with its associated details.


### Building a Business Query

#### Step 1: Start with a simple SELECT query
SELECT
    donors.first_name AS "First Name",
    donors.last_name AS "Last Name",
    donors.email AS "Email"
FROM donors;































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


