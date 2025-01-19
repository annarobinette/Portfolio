# Rabble Sports Analytics Pipeline

## Data Pipeline Implementation

## Initial Thoughts

After looking at the booking platform, I understood that the data was available in the following 8 files. There were downloaded in csv for ease of transmitting to other data systems. The files were:

1. peopleinfo.csv - Core player database
    - Contains basic personal information about players
    - Includes contact details, address information, and attendance statistics
    - Acts as the central player registry with joining dates and activity records

2. eventattendance.csv - Detailed event participation records
    - Tracks who attended which events
    - Records venue, timing, and whether passes were used
    - Links players to specific events and tracks their attendance status

3. clubpayments.csv - Financial transaction records
    - Records all payments made by players
    - Includes fee breakdowns between club, payment provider, and platform
    - Tracks payment methods and timestamps

4. leadersattendees.csv - Event leadership and attendance tracking
    - Links events to their leaders
    - Tracks sign-ups, attendance, and no-shows
    - Records leader information for each event

5. assocclubusage.csv - Venue and timing records
    - Tracks facility usage and event scheduling
    - Records peak vs off-peak usage
    - Contains venue-specific information and event durations

6. clubcomments.csv - Player feedback and ratings
    - Stores event feedback and ratings from players
    - Includes comments tied to specific events and leaders
    - Records when feedback was provided

7. gdproptin.csv - Marketing consent records
    - Tracks marketing preferences and consent
    - Links players to their communication preferences
    - GDPR compliance related data

8. followersummary.csv - Player engagement metrics
    - Aggregates player activity and engagement
    - Tracks total spend and participation
    - Records which clubs players follow

### Entity Relationship Diagram
```mermaid
erDiagram
    peopleinfo ||--o{ eventattendance : "attends"
    peopleinfo ||--o{ clubpayments : "makes"
    peopleinfo ||--o{ gdproptin : "opts_into"
    peopleinfo ||--o{ clubcomments : "leaves"
    peopleinfo ||--o{ followersummary : "summarizes"
    
    peopleinfo {
        string address_line_1
        string address_line_2
        string town
        string postcode
        string phone_number
        float country
        string first_name
        string last_name
        string email
        string joined
        string first_attend
        string most_recent
        int num_attend
    }

    eventattendance {
        string ClubID
        string Club
        string EventID
        string EventTitle
        string Venue
        string StartTime
        string Month
        string Year
        string UserID
        string Attendee
        string Email
        string Points
        string Leader
        string Seen
        string HasPass
        string Passused
        string WhenSeen
        string WhenAdded
    }

    assocclubusage ||--o{ eventattendance : "tracks"
    assocclubusage {
        string EventID
        string Title
        string Associated_Club
        string VenueID
        string Venue
        string StartTime
        string StartDate
        string EndTime
        string Day
        string Duration
        string Peak
        string Off_Peak
    }

    clubpayments {
        int PaymentID
        int ClubID
        string Club
        int UserID
        string Firstname
        string Lastname
        float Payment
        string Payment_Method
        float Collected_for_Club
        float Payment_Provider_Fee
        float Makesweat_Fee
        string currency
        string CreatedTime
    }

    gdproptin {
        int ClubID
        string Club
        int UserID
        string Firstname
        string Lastname
        string Email
    }

    leadersattendees ||--o{ eventattendance : "leads"
    leadersattendees {
        string Club
        string EventID
        string Title
        string StartTime
        string StartDate
        string Signed_up
        string Seen
        string Did_Not_Attend
        string Leaders
        string Leader_First_name
        string Leader_Last_name
    }

    clubcomments {
        string Club
        string First_name
        string Last_name
        string Email
        string Event_title
        string Event_leaders
        string Event_start_time
        string Attendees
        string Pass_type_used
        string Rating
        string Comment
        string Time_created
        string Event_time_zone
    }

    followersummary {
        int Makesweat_ID
        string Firstname
        string Lastname
        string Email
        string Followed_Clubs
        string Signup_date
        string First_event
        string Latest_past_event
        float Enrollment_count
        float Pass_use_count
        float Total_spend
    }
```
(also available to view [here](../images/bookingplatform_erd.png))

After extracting the data, the data will need transforming into a more logical data structure.

### MakeSweat API integration

### Automated data extraction
### GCP storage configuration