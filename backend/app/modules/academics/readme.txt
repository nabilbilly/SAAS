Academic Year Management Updates
Goal Description
Enhance 
AcademicYear
 resource to include start_date and end_date, and enforce logic ensuring only one academic year is Active at a time. The start_date and end_date must be valid before activation.

User Review Required
IMPORTANT

This change involves modifying the database schema. Since alembic is not configured, a manual migration script upgrade_academic_year.py will be created and executed to add start_date and end_date columns to the existing table without data loss.

Proposed Changes
Database Migration
[NEW] 
backend/upgrade_academic_year.py
Script to add start_date and end_date columns to academicyears (or appropriate table name) if they don't exist.
Backend Code
[MODIFY] 
backend/app/modules/academics/models.py
Add start_date (Date, nullable=True) and end_date (Date, nullable=True).
[MODIFY] 
backend/app/modules/academics/schemas.py
Add start_date and end_date to 
AcademicYearBase
, 
AcademicYearCreate
, AcademicYearUpdate, and 
AcademicYearResponse
.
[MODIFY] 
backend/app/modules/academics/router.py
Update 
create_academic_year
 to accept dates.
Update 
update_year_status
 or create a generic update endpoint:
Validate start_date and end_date are present and valid (start < end) before setting status to Active.
If status is being set to Active, check if any other year is Active. If so, reject or handle accordingly (User said "Only one academic year can be Active"). We will reject with 400.
Verification Plan
Automated Tests

Run upgrade_academic_year.py and check output.
Create a test script verify_academic_year.py to:
Create a Draft year with dates.
Try to Activate it (should succeed).
Create another Draft year.
Try to Activate the second one (should fail).
Archive the first one.
Activate the second one (should succeed).