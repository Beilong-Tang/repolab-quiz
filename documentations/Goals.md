# Simple Judge

## Feature
- Web GUI
- Multi-User: admin system
    - Students
    - Teachers
- Markdown input format and auto generation
- SSO compatiablity

## Framework
- Django

## Due
- 2022-08-15

## Milestone
- Web GUI
    - Basic
    - css
    - Javascript
    - Infomation vistualization
    - Import and export
- Markdown translation: Markdown to HTML
    - Formatting
    - Converting
    - Rendering
- Answer converter: Allow answers that is corret correct
- Multi-User
- Single-sign On
- Deployment
    - HTTP-server
    - Web app
    - DB

## Possible roadblock
- Store pictures in database

## DataBase Schema
This is a possible database layout. However, not every function needs to be realized.

- Student
    - Unique ID
    - Username
    - Password
    - Nickname
    - E-mail Address
    - Courses
        - Teacher
        - Course Schedule
        - Privilage Level
        - Grinding process

- Teacher
    - Unique ID
    - Username
    - Password
    - Nickname
    - E-mail address
    - Courses
        - Privilage Level
        - Course
        - Students

- Question and Answer
    - Question ID
    - Question Detail (Including Pictures)
    - Hint
    - Answer Type (Multiple Choice? Filling the Blank?)
    - Correct Answer
    - Explanation
    - Owner (Which teacher)
    - Create Time

- Question and Answer (Raw)
    - ID
    - Original Markdown
    - Owner
    - Time imported

- Quiz Sheet
    - Quiz ID
    - Time Created
    - Description
    - Total credit
    - Question ID
        - Time Limit
        - Credit
        - Try and Error

- Course schedule
    - Milestone
        - Time
        - Quiz Sheet
            - Time unhidden
            - Due
            - Credit
        - Description
    - Start time
    - Finish time
    - Description
    - Teacher

- Grinding process
    - Question ID
        - Answer state
        - Last answer
        - Start time
        - Finish time

