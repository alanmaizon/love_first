# **❤️ Love**

---

## **Concept Overview**  
**Theme:** A platform where users can explore and donate to various charity organizations tied to a couple's values.  
**Objective:**  
- Celebrate love by inspiring generosity.  
- Provide a seamless user experience for exploring charities and donating.  

---

## **Front-End Features**  

### 1. **Home Page (Landing Page)**  
- A hero section introducing the mission.  
- Links/buttons for logging in, exploring charities, and donating.  
- Display the wedding date with a countdown.  
- Highlight charity statistics (e.g., total donations).  

### 2. **User Authentication**  
- Registration: Name, email, password.  
- Login/Logout: Use Django Rest Framework for token-based authentication.  

### 3. **Dashboard**  
- Display personalized greetings.  
- Show donation history and progress.  
- Enable users to set donation goals.  

### 4. **Charity Pages (CRUD Features)**  
- Explore three charities with descriptions, images, and goals.  
- Allow users (admins) to create/update/delete charity profiles.  
- Enable commenting or "likes" on charities as a bonus feature.  

### 5. **Responsive Design**  
- Use bootstrap and CSS for a modern, responsive design.
- Ensure compatibility across devices.  

### 6. **API Integration**  
- **External API:** Display live progress using an external API, e.g., PayPal or Stripe for secure payments.  

---

## **Back-End Features**  

### 1. **Django Server**  
- RESTful API with Django Rest Framework.  
- Serve data to the React front-end.  

### 2. **Database**  
- PostgreSQL for scalable and reliable data management.  
- Store user profiles, charity data, and donation transactions.  

### 3. **User Authentication & Authorization**  
- Secure user login with hashed passwords.  
- Assign roles (admin, authenticated user, guest).  

### 4. **Donation Management**  
- CRUD functionality for donations.  
- Generate donation receipts.  

### 5. **Automated Testing**  
- Use Django's `unittest` framework to test API endpoints and functionality.  

---

## **Tools & Technologies**  

### **Front-End:**  
- React with React Router.  
- Axios for API calls.   

### **Back-End:**  
- Django with Django Rest Framework.  
- PostgreSQL database.  

### **Version Control & Deployment:**  
- Git for version control.  
- Deploy front-end and back-end with Render.  

---

Final Project - UCD PA - Alan Maizon

# Final Project: Love That Gives Back

**Objective:**  
Help me step by step to create the backend and frontend locally using Django with Bootstrap. The project will use Django’s built‑in authentication (Session Auth) with PostgreSQL, and it will be deployed to Render.com.

---

## User Roles and Storyboards

### 1. Guest User (Wedding Guest)
**Scenario:** Maria is attending her friend's wedding and wants to make a donation in honor of the couple instead of buying a traditional gift.

**User Journey:**
1. **Visit Website:** Maria lands on the home page and sees the donation initiative.
2. **Selects a Charity:** She chooses one of the couple’s supported charities.
3. **Enters Donation Details:** Maria enters her name, donation amount, and a personal message.
4. **Confirms Donation:** She reviews the manual bank transfer details and submits the donation.
5. **Receives Confirmation:** Maria gets a success message and can share her donation.

---

### 2. Wedding Couple (Recipients)
**Scenario:** Alan and Anna want to track all received donations and manage the charities they support.

**User Journey:**
1. **Register:** The couple registers as a single user (with an extended Profile) on the platform.
2. **Login:** They log in to access their private dashboard.
3. **Manage Charities:** They can add or update the list of charities they want to support.
4. **View Donations:** They see a list of confirmed donations (along with donor messages) filtered by their supported charities.
5. **Confirm Payments:** They manually confirm received payments (if necessary) or use auto-reminders.
6. **Share Gratitude:** They thank donors via email or social media.

---

### 3. Admin (Platform Manager)
**Scenario:** An administrator oversees the entire donation system.

**User Journey:**
1. **Login:** The admin logs in (using Django’s admin interface or a dedicated dashboard).
2. **View Statistics:** The admin can see total donation amounts, top contributors, and overall platform metrics.
3. **Manage Donations:** The admin confirms or marks donations as failed.
4. **Manage Users & Charities:** The admin ensures that charities and transactions are legitimate.
5. **Generate Reports:** The admin extracts donation data for transparency and dispute resolution.

---

## Features Breakdown with Dependencies

| **Feature**                      | **Depends On**                            |
| -------------------------------- | ----------------------------------------- |
| User Authentication              | Django’s built‑in auth, Registration/Login  |
| Donation Form                    | User authentication (optional), Charity List |
| Manual Payment Instructions      | Backend processing of donation records    |
| Donation Confirmation            | Admin panel to verify and update payments |
| Guest Donation Flow              | No login required; relies on Charity & Donation models |
| Couple Dashboard                 | Extended Profile (one-to‑one with User) and Donation filtering by supported charities |
| Admin Dashboard                  | Donations & Charity management, analytics  |
| Analytics & Reporting            | Aggregation of Donation and Charity data  |

### Flow of Dependencies

1. **Authentication:**  
   - Guests can donate without logging in.
   - Wedding couples register as a single user and extend their data via a Profile.
   - Admins log in with elevated privileges.
   
2. **Profile Management (Couple Dashboard):**  
   - The Profile (or CoupleProfile) model extends User and stores wedding date, bio, supported charities, etc.
   - Couples can update which charities they support.
   
3. **Charity Management:**  
   - The Charity model holds data on all charities.
   - Couples can add new charities (if the one they want isn’t available), which then become available globally.
   
4. **Donation Process:**  
   - The Donation model captures guest donations, linking each donation to a charity (and optionally a user).
   - The donation form and confirmation page rely on valid Charity data.
   
5. **Analytics:**  
   - Aggregated donation data (summing confirmed donations, calculating splits, trends) is used by the Admin Dashboard.
   - Charts (using matplotlib) visualize trends, donation splits, and per-charity allocations.
   
6. **Overall Flow:**  
   - **Guest:** Home → Select Couple → Choose Charity → Donation Form → Payment Instructions → Confirmation  
   - **Couple:** Register/Login → Manage Profile & Charities → View Donations → Confirm Payment → Share Gratitude  
   - **Admin:** Login → Dashboard → Manage Donations/Charities → Generate Reports

---

## Sitemap with Navigation Logic

```
Home → User Profile (if logged in) → Donation Page → Confirmation Page 
     → Dashboard (Guest: view donation history, Couple: manage profile and charities) → Admin Panel (for admins)
```

**Navigation Considerations:**
- **Guests:** Can explore and donate without authentication.
- **Couples:** Have a dedicated dashboard to manage their profile, supported charities, and view donations.
- **Admins:** Access a separate panel with global controls and reporting tools.

---

## ER Diagram

```mermaid
erDiagram
    USER {
      int id PK
      string username
      string email
    }
    PROFILE {
      int id PK
      date wedding_date
      string bio
      string location
      string profile_picture
      json social_media_links
      string contact_email
      string contact_phone
    }
    CHARITY {
      int id PK
      string name
      string description
      string website
      string logo
    }
    DONATION {
      int id PK
      string donor_name
      string donor_email
      decimal amount
      string message
      string status "pending/confirmed/failed"
      datetime created_at
      datetime updated_at
      string stripe_payment_id "optional"
    }
    
    USER ||--|| PROFILE : "has"
    PROFILE }o--o{ CHARITY : "supports"
    CHARITY ||--o{ DONATION : "receives"
```

---

## Sitemap

```mermaid
mindmap
  root((Love That Gives Back))
      About / How It Works (About Us)
      Registration Page (Register)
        Create Profile
      Login Page (Login)
      Home Page (Home)
        Select Cause (Charities)
          Donation Form Page (Donate)
            Payment Instructions Page
           Donation Confirmation Page
      Couple Dashboard (Dashboard)
        Couple's Profile (Settings)
          Edit Profile
          Manage Supported Charities (Charities)
            Add New Charity
            View Supported Charities
              Edit Selected Charities
        View Donations (Donations)
          List of Confirmed Donations
          Donation Details Page
      Admin Dashboard (Admin Panel)
        Manage Donations
          (Confirm / Fail)
        View Overall Donation Statistics (Analytics/Reports)
          Charts
          Export
        Manage Users
        Manage Charities
```

---

## User Flow

```mermaid
flowchart TD
    A[Visit Home Page] --> B{User Type?}
    B -- Guest --> C[Select Couple Profile]
    C --> D[Choose Supported Charity]
    D --> E[Fill Out Donation Form]
    E --> F[Review Payment Instructions]
    F --> G[Donation Confirmation]
    
    B -- Couple --> H[Register / Login]
    H --> I[Manage Profile]
    I --> J[Edit Profile Details]
    J --> K[(Wedding Date, Bio, Location)]
    I --> L[Manage Supported Charities]
    L --> M[Add New Charity]
    M --> N[(Name, Description, Website)]
    L --> O[View/Update Selected Charities]
    I --> P[View Donations]
    P --> Q[List of Confirmed Donations]
    Q --> R[Donation Details]
    
    B -- Admin --> S[Admin Login]
    S --> T[Admin Dashboard]
    T --> U[Manage Donations]
    T --> V[View Statistics & Analytics]
    V --> W[(Percentage Charts, Donation Trends)]
    T --> X[Manage Users & Charities]
```
