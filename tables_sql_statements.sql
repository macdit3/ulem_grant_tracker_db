-- Create donors table if it doesn't exist
CREATE TABLE IF NOT EXISTS donors (
                                      id SERIAL PRIMARY KEY,
                                      donor_type VARCHAR(20) NOT NULL,
                                      first_name VARCHAR(100),
                                      last_name VARCHAR(100),
                                      organization_name VARCHAR(200),
                                      email VARCHAR(255),
                                      phone VARCHAR(20),
                                      address_line1 VARCHAR(255),
                                      address_line2 VARCHAR(255),
                                      city VARCHAR(100),
                                      state VARCHAR(100),
                                      postal_code VARCHAR(20),
                                      country VARCHAR(100),
                                      preferred_contact_method VARCHAR(20),
                                      notes TEXT,
                                      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                      updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create programs table if it doesn't exist
CREATE TABLE IF NOT EXISTS programs (
                                        id SERIAL PRIMARY KEY,
                                        name VARCHAR(200) NOT NULL,
                                        description TEXT,
                                        start_date DATE,
                                        end_date DATE,
                                        budget DECIMAL(10,2),
									    goal_amount DECIMAL(10,2),
										current_progress DECIMAL(10,2),
                                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create donations table if it doesn't exist
CREATE TABLE IF NOT EXISTS donations (
                                         id SERIAL PRIMARY KEY,
                                         donor_id INTEGER REFERENCES donors(id),
                                         program_id INTEGER REFERENCES programs(id),
                                         amount DECIMAL(10,2) NOT NULL,
                                         donation_date DATE NOT NULL,
                                         payment_method VARCHAR(50),
                                         transaction_id VARCHAR(100),
                                         is_tax_deductible BOOLEAN DEFAULT FALSE,
                                         notes TEXT,
                                         created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                         updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create pledges table if it doesn't exist
CREATE TABLE IF NOT EXISTS pledges (
                                       id SERIAL PRIMARY KEY,
                                       donor_id INTEGER REFERENCES donors(id),
                                       program_id INTEGER REFERENCES programs(id),
                                       amount DECIMAL(10,2) NOT NULL,
                                       pledge_date DATE NOT NULL,
                                       fulfillment_date DATE,
                                       status VARCHAR(50),
									   amount_fulfilled DECIMAL(10,2) NOT NULL,
                                       notes TEXT,
                                       created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                       updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create tax_receipts table if it doesn't exist
CREATE TABLE IF NOT EXISTS tax_receipts (
                                            id SERIAL PRIMARY KEY,
                                            donor_id INTEGER REFERENCES donations(id),
											year_donated DATE,
										    total_amount DECIMAL(10,2) NOT NULL,
                                            generated_date DATE NOT NULL,
                                            sent_date DATE,
                                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create thank_you_notes table if it doesn't exist
CREATE TABLE IF NOT EXISTS thank_you_notes (
                                               id SERIAL PRIMARY KEY,
											   donor_id INTEGER REFERENCES donors(id,
                                               donation_id INTEGER REFERENCES donations(id),
                                               sent_date DATE,
                                               method VARCHAR(50),
                                               template_used VARCHAR(100),
                                               notes TEXT,
                                               created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                               updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);