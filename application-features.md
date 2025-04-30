## Summary
I've created a comprehensive FastAPI application that provides APIs for all the entities in your database:
1. **Donors** - Full CRUD operations for managing donor information
2. **Programs** - Full CRUD operations for fundraising programs/campaigns
3. **Donations** - Full CRUD operations for donations with automatic program progress updates
4. **Pledges** - Full CRUD operations for managing donation pledges
5. **Tax Receipts** - Full CRUD operations for managing tax receipts
6. **Thank You Notes** - Full CRUD operations for tracking thank you notes sent to donors

Additionally, I've included several reporting endpoints that provide valuable insights:
- Donation summary by program
- Donation summary by donor
- List of unfulfilled pledges
- List of pending thank you notes
- Ability to generate tax receipts for a specific year

### Key Features:
1. **Data Validation** - Using Pydantic models for request/response validation
2. **Relationships** - Properly defined SQLAlchemy relationships between tables
3. **Automatic Progress Tracking** - Updates program fundraising progress when donations are created/modified/deleted
4. **Filtering** - All list endpoints support filtering by various parameters
5. **Error Handling** - Proper validation and error handling for all operations
6. **Auto-creation of Tables** - Tables are automatically created on startup if they don't exist
