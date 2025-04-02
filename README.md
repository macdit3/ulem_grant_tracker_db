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
    git clone https://github.com/your-repo/concert_ticket_system_2.git
    ```
2. Navigate to the project directory:
    ```bash
    cd concert_ticket_system_2
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


