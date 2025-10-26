**AI-Powered Hunger Heatmap with QR-Based Relief Verification System**
Project Overview:
  This project aims to support United Nations Sustainable Development Goal (SDG) 2 – Zero Hunger by leveraging Artificial Intelligence (AI) and Blockchain Technology.
It predicts hunger-prone zones using real-world data such as rainfall, crop failures, job losses, and food prices — and ensures fair food distribution through QR-based digital tokens.
The system is built as a Flask web application that generates a live Hunger Heatmap, manages food token distribution, verifies beneficiaries through QR code scanning, and records every transaction transparently.

Tech Stack:
Component	Technology Used Are
Frontend	HTML, CSS, JavaScript
Backend	Python Flask
Database	JSON / CSV file storage
AI Tools	Pandas, NumPy, Scikit-Learn
Visualization	Google Maps API, Matplotlib
Additional	gTTS (Text-to-Speech), QRCode Library

**🚀 How to Run the Project**
**Step 1: Install Python**

Ensure that Python 3.9+ is installed.
Check by running:
python --version

**Step 2: Install Required Packages**

Navigate to the Source_Code folder and install dependencies:
pip install -r requirements.txt

If requirements.txt is missing, install manually:
pip install flask pandas numpy scikit-learn qrcode gtts

**Step 3: Run the Application**
cd Source_Code
python app.py

You will see:
 * Running on http://127.0.0.1:5000/

**Step 4: Open in Browser**

Go to your browser and open:
👉 http://127.0.0.1:5000

🔑 Login Credentials
User Role	    Username	    Password
Admin	        admin	        admin123
User	        user	        user123
