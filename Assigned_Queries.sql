-- Building Advanced SQL Queries for Business Applications

-- Step 1: Start with a simple SELECT Query
SELECT
    -- Display table headers nicely
    donors.first_name AS "First Name",
    donors.last_name AS "Last Name",
    donors.email AS "Email"
FROM donors
-- Filter out records where first_name or last_name is NULL
WHERE first_name IS NOT NULL AND last_name IS NOT NULL;


-- Display all donors in our database
SELECT *
FROM donors
WHERE state != 'CA';

-- Step 2: Join the donations table to access donation amounts
SELECT
    dn.first_name AS "First Name",
    dn.last_name AS "Last Name",
    dn.email AS "Email",
    dt.amount AS "Amount Donated"

FROM donors dn
INNER JOIN donations dt on dn.id = dt.id;
--WHERE dn.email like '%futurefoundation@example.com%';


-- Step 3: Add filtering condition
-- only return those who donated more than $ 500
SELECT
    donors.first_name AS "First Name",
    donors.last_name AS "Last Name",
    donors.email AS "Email",
    donors.donor_type AS "Donor Type",
    donations.amount AS "Amount Donated"
FROM donors
INNER JOIN donations ON donors.id = donations.id
WHERE
    donations.amount > 500
     AND donors.donor_type = 'individual';
-- Note: The above query filters for individual donors
-- who donated more than $500. You can adjust the amount or donor type as needed.

-- Step 4: Join the thank_you_notes table
SELECT
    donors.first_name AS "First Name",
    donors.last_name AS "Last Name",
    donors.email AS "Email",
    donors.donor_type AS "Donor Type",
    donations.amount AS "Amount Donated",
    thank_you_notes.sent_date AS "Sent On"
FROM donors
INNER JOIN donations ON donors.id = donations.donor_id
INNER JOIN thank_you_notes ON donations.id = thank_you_notes.donation_id
WHERE
    donations.amount > 500
    AND donors.donor_type = 'individual';

-- Advanced Query Concepts: Finding Missing Data
-- 1) Find donors who have donated more than $500 but do not have a thank you note sent
SELECT
    donors.first_name AS "First Name",
    donors.last_name AS "Last Name",
    donors.email AS "Email",
    donors.donor_type AS "Donor Type",
    donations.amount AS "Amount Donated"
FROM donors
INNER JOIN donations ON donors.id = donations.donor_id
LEFT JOIN thank_you_notes ON donations.id = thank_you_notes.donation_id
WHERE
    donations.amount > 500
    AND donors.donor_type = 'individual'
    AND thank_you_notes.sent_date IS NULL; -- This condition filters out those with a sent thank you note


-- 2) LEFT JOIN with NULL check - alternative approach

SELECT
    donors.first_name AS "First Name",
    donors.last_name AS "Last Name",
    donors.email AS "Email",
    donors.donor_type AS "Donor Type",
    donations.amount AS "Amount Donated"
FROM donors
INNER JOIN donations ON donors.id = donations.donor_id
LEFT JOIN thank_you_notes ON donations.id = thank_you_notes.donation_id
WHERE
    donations.amount > 500
    AND donors.donor_type = 'individual'
    AND thank_you_notes.id IS NULL;


-- Real-World Applications:
-- The skills we're practicing directly translate to actual business scenarios:

-- 1. **E-commerce**: Finding customers who purchased but didn't receive a confirmation email
-- 2. **Healthcare**: Identifying patients who haven't completed follow-up appointments
-- 3. **Finance**: Discovering transactions that haven't been reconciled
-- 4. **Education**: Locating students who haven't submitted assignments
-- 5. **Marketing**: Targeting customers who haven't engaged with recent campaigns


-- Step by step: answering Business Questions with SQL
-- 1) Display first name and last name of the donors.
SELECT
    dn.first_name,
    dn.last_name
FROM donors AS dn;

-- 2) Join related tables
SELECT
    dn.first_name AS "First Name",
    dn.last_name AS "Last Name",
    dt.amount AS "Amount Donated"

FROM donors AS dn
INNER JOIN donations AS dt on dn.id = dt.donor_id;

-- 3) Adding filtering conditions

SELECT
    dn.first_name AS "First Name",
    dn.last_name AS "Last Name",
    dt.amount AS "Amount Donated"

FROM donors AS dn
INNER JOIN donations dt on dn.id = dt.donor_id
WHERE
    dn.first_name IS NOT NULL
    AND dt.amount > 500;


-- 4) Sort and Limit Results
SELECT
    dn.first_name AS "First Name"
    , dn.last_name AS "Last Name"
    , dt.amount AS "Amount Donated"

FROM
    donors AS dn
INNER JOIN
        donations AS dt ON dn.id = dt.donor_id

WHERE
    dn.first_name IS NOT NULL
    AND dt.amount > 500
ORDER BY
     dt.amount DESC
LIMIT 10;


-- Challenge problem: Practice Exercise
-- give all donors who have donated $500+ but we haven't sent a thank-you note
-- @TODO: your task is to solve the problem above using a "LEFT JOIN"
-- 1 . grab this code base and dataset from ulem_grant_tracker
-- 2. import this "ulem_grant_initial-data.sql" into your data (be sure that docker is running
-- 3. Open this file in pycharm and try to write the query for this from

SELECT
     -- all columns
      dn.id         AS "Donor ID"
      ,dn.first_name AS "First Name"
     ,dn.last_name  AS "Last Name"
     ,dn.donor_type AS "Donor Type"
     ,dt.amount     AS "Amount Donated"
     ,pg.description AS "Program Description"
     ,tyn.notes
     ,tyn.sent_date

FROM donors dn
-- INNER JOIN
         inner join donations dt on dn.id = dt.donor_id
         inner join public.programs pg on pg.id = dt.program_id
         left join public.thank_you_notes tyn on dn.id = tyn.donor_id
WHERE dn.first_name is not null
        AND dt.amount > 500
        AND tyn.sent_date is null
ORDER BY dt.amount DESC
LIMIT 10;


SELECT *
FROM donors
WHERE donors.id = 4;

SELECT *
FROM thank_you_notes
WHERE donor_id= 3;






















