# **📌 Planning Analysis & Site Map Presentation**  

---

## **1. Site Map**  

Below is the **high-level structure** of the web application:  

```
📍 Home (Landing Page)
  ├── Hero Section (Mission & Call-to-Action)
  ├── Wedding Date Countdown
  ├── Charity Highlights  
  ├── Login/Register  

📍 Authentication  
  ├── Register (Name, Email, Password)  
  ├── Login (JWT Authentication)  
  ├── Logout  

📍 Dashboard (Authenticated Users)  
  ├── Personalized Greeting  
  ├── Donation Progress & History  
  ├── Set Donation Goals  

📍 Charity Pages (CRUD Functionality)  
  ├── View Available Charities  
  ├── Donate to a Charity (Stripe API)  
  ├── Admin: Create/Edit/Delete Charity Profiles  

📍 Additional Pages  
  ├── About Us  
  ├── Contact Page  
  ├── Terms & Conditions  
```

---

## **2. Planning Analysis Sheet**  

| **Feature**            | **Priority** | **Description** |
|------------------------|-------------|----------------|
| User Authentication    | Essential   | Secure login/register with JWT |
| Dashboard             | Essential   | Displays donation progress |
| Charity Exploration   | Essential   | Users browse available charities |
| Donations (Stripe API) | Essential   | Secure donation processing |
| Charity CRUD (Admin)   | Essential   | Admins manage charities |
| Comments/Likes        | Optional    | Users interact with charities |
| Wedding Date Countdown | Optional    | Displays time until wedding |
| User Profiles         | Optional    | Users customize profile |

---

## **3. User Roles & Permissions**  

| **User Role**         | **Permissions** |
|----------------------|----------------|
| **Guest**           | View charities, but cannot donate or comment |
| **Authenticated User** | Donate, track donation history, comment on charities |
| **Admin**           | Full CRUD access for charities, manage donations |

---

## **4. Anticipated Challenges & Solutions**  

| **Challenge**                        | **Potential Solution** |
|---------------------------------------|------------------------|
| **Secure Authentication** | Implement JWT and hashed passwords |
| **Payment Integration Complexity** | Use Stripe API with well-documented SDK |
| **Scalability for More Charities** | Optimize database queries and API performance |
| **Ensuring a Seamless UX/UI** | Conduct usability testing and improve CSS |

---

## **5. User Flow Diagram**  

```
[Landing Page] --> [Login/Register] --> [Dashboard] --> [Browse Charities] --> [Donate] --> [Track Progress]
```

🛠 **Admin Flow:**  
```
[Admin Dashboard] --> [Manage Charities] --> [Edit/Delete Charities] --> [View Donations]
```

This structured approach ensures **smooth navigation** and **optimal user experience**! 💡