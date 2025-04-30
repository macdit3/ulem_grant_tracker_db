-- Sample Data for Donor Management Database

-- 1. DONORS table
INSERT INTO public.donors (donor_type, first_name, last_name, organization_name, email, phone, address_line1, address_line2, city, state, postal_code, country, preferred_contact_method, notes)
VALUES
    ('individual', 'John', 'Smith', NULL, 'john.smith@email.com', '555-123-4567', '123 Main St', 'Apt 4B', 'New York', 'NY', '10001', 'USA', 'email', 'Regular donor since 2018, prefers quarterly communications'),
    ('individual', 'Maria', 'Garcia', NULL, 'mgarcia@example.com', '555-987-6543', '789 Oak Avenue', NULL, 'Chicago', 'IL', '60601', 'USA', 'phone', 'Interested in education programs specifically'),
    ('organization', NULL, NULL, 'Bright Future Foundation', 'donations@brightfuture.org', '555-444-3333', '567 Corporate Pkwy', 'Suite 300', 'Boston', 'MA', '02108', 'USA', 'email', 'Annual corporate matching program'),
    ('individual', 'Robert', 'Johnson', NULL, 'rjohnson@mail.com', '555-222-1111', '42 Sunset Blvd', NULL, 'Los Angeles', 'CA', '90210', 'USA', 'mail', 'Major donor, send personalized communications'),
    ('organization', NULL, NULL, 'Community Trust Bank', 'giving@ctbank.com', '555-777-8888', '100 Financial Way', '15th Floor', 'Dallas', 'TX', '75201', 'USA', 'email', 'Provides grants for community programs');

-- 2. PROGRAMS table
INSERT INTO public.programs (name, description, start_date, end_date, budget, goal_amount, current_progress)
VALUES
    ('Youth Education Initiative', 'Providing after-school tutoring and educational resources to underserved communities', '2023-01-01', '2023-12-31', 125000.00, 150000.00, 87500.00),
    ('Community Health Outreach', 'Mobile health screenings and educational workshops in rural areas', '2023-03-15', '2023-11-30', 75000.00, 100000.00, 62000.00),
    ('Arts for All', 'Making arts education accessible to children from low-income families', '2023-06-01', '2024-05-31', 50000.00, 60000.00, 22500.00),
    ('Senior Support Network', 'Providing meals, transportation, and companionship to elderly residents', '2023-01-01', '2023-12-31', 95000.00, 120000.00, 78000.00),
    ('Environmental Restoration Project', 'Restoring local watershed and creating educational nature trails', '2023-04-22', '2023-10-15', 85000.00, 95000.00, 45000.00);

-- 3. DONATIONS table
INSERT INTO public.donations (donor_id, program_id, amount, donation_date, payment_method, transaction_id, is_tax_deductible, notes)
VALUES
    (1, 1, 500.00, '2023-02-15', 'credit_card', 'TXN-123456', true, 'Monthly recurring donation'),
    (3, 2, 10000.00, '2023-04-10', 'check', 'CHK-789012', true, 'Annual corporate contribution'),
    (2, 1, 250.00, '2023-03-22', 'paypal', 'PP-345678', true, 'First-time donor'),
    (4, 4, 5000.00, '2023-01-30', 'wire_transfer', 'WT-901234', true, 'Specified for senior meal program'),
    (5, 3, 7500.00, '2023-07-15', 'check', 'CHK-567890', true, 'Matching gift program');

-- 4. PLEDGES table
INSERT INTO public.pledges (donor_id, program_id, amount, pledge_date, fulfillment_date, status, amount_fulfilled, notes)
VALUES
    (4, 4, 10000.00, '2023-01-15', '2023-01-30', 'fulfilled', 10000.00, 'Fulfilled ahead of schedule'),
    (3, 2, 25000.00, '2023-03-01', '2023-04-10', 'fulfilled', 25000.00, 'Part of annual giving commitment'),
    (1, 5, 1200.00, '2023-05-10', NULL, 'pending', 500.00, 'Monthly installments of $100'),
    (5, 3, 15000.00, '2023-06-01', '2023-07-15', 'partially_fulfilled', 7500.00, 'Remainder due by year-end'),
    (2, 1, 1000.00, '2023-02-28', '2023-03-22', 'fulfilled', 1000.00, 'One-time pledge');

-- 5. TAX_RECEIPTS table
INSERT INTO public.tax_receipts (donor_id, year_donated, total_amount, generated_date, sent_date)
VALUES
    (1, '2022-12-31', 2400.00, '2023-01-15', '2023-01-20'),
    (3, '2022-12-31', 35000.00, '2023-01-15', '2023-01-20'),
    (4, '2022-12-31', 12500.00, '2023-01-15', '2023-01-20'),
    (2, '2022-12-31', 750.00, '2023-01-15', '2023-01-20'),
    (5, '2022-12-31', 20000.00, '2023-01-15', '2023-01-20');

-- 6. THANK_YOU_NOTES table
INSERT INTO public.thank_you_notes (donor_id, donation_id, sent_date, method, template_used, notes)
VALUES
    (1, 1, '2023-02-16', 'email', 'monthly_donor', 'Personalized with education program updates'),
    (3, 2, '2023-04-12', 'mail', 'corporate_donor', 'Included annual impact report'),
    (2, 3, '2023-03-24', 'email', 'first_time_donor', 'Included welcome packet information'),
    (4, 4, '2023-02-02', 'mail', 'major_donor', 'Hand-signed by executive director'),
    (5, 5, '2023-07-17', 'email', 'corporate_donor', 'Included photo from arts program');

