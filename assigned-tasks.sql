-- Query 1: List all donors and their email addresses
SELECT first_name, last_name, organization_name, email
FROM donors;


-- Query 2: List all programs with budgets over $10,000
SELECT name, budget
FROM programs
WHERE budget > 10000
ORDER BY budget DESC;

-- Query 3: Show all donations in descending order by amount
SELECT *
FROM donations
ORDER BY amount DESC;



-- Find all donors where the email contains "example.com"
SELECT *
FROM donors
WHERE email LIKE '%example.com%';

-- Find all programs that have the word "Youth" in their name or description
SELECT *
FROM programs
WHERE name LIKE '%Youth%' OR description LIKE '%Youth%';

-- Find all donations made in 2023
SELECT *
FROM donations
WHERE EXTRACT(YEAR FROM donation_date) = 2023;
-- Alternative if your database uses a different date function:
-- SELECT *
-- FROM Donations
-- WHERE DonationDate BETWEEN '2023-01-01' AND '2023-12-31';


-- List the total amount donated by each donor
SELECT
    d.id,
    d.first_name,
    d.last_name,
    d.organization_name,
    SUM(don.amount) AS TotalDonated
FROM
    donors d
JOIN
    donations don ON d.id = don.donor_id
GROUP BY
    d.id, d.first_name, d.last_name, d.organization_name
ORDER BY
    TotalDonated DESC;


-- Find the program that has received the most total donations
SELECT
    p.id,
    p.name,
    SUM(don.Amount) AS TotalDonations
FROM
    programs p
JOIN
    donations don ON p.id = don.program_id
GROUP BY
    p.id, p.name
ORDER BY
    TotalDonations DESC;


-- For SQL Server, use TOP 1 instead of LIMIT:
-- SELECT TOP 1
--     p.ProgramID,
--     p.ProgramName,
--     SUM(don.Amount) AS TotalDonations
-- FROM...

-- List all donors (individuals or organization) who have made more than one donation
SELECT
    d.id,
    d.first_name,
    d.last_name,
    d.organization_name,
    COUNT(don.id) AS DonationCount
FROM
    donors d
JOIN
    donations don ON d.id = don.donor_id
GROUP BY
    d.id, d.first_name, d.last_name, d.organization_name
HAVING
    COUNT(don.id) > 1
ORDER BY
    DonationCount DESC;

-- Create a report showing each program, the total amount donated to that program, and what percentage that represents of all donations

WITH TotalDonations AS (
    SELECT SUM(amount) AS GrandTotal
    FROM donations
)
SELECT
    p.id,
    p.name,
    SUM(d.amount) AS TotalDonated,
    ROUND((SUM(d.amount) / (SELECT GrandTotal FROM TotalDonations)) * 100, 2) AS PercentageOfAllDonations
FROM
    programs p
JOIN
    donations d ON p.id = d.program_id
GROUP BY
    p.id, p.name
ORDER BY
        TotalDonated DESC;