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
