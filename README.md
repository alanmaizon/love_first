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
