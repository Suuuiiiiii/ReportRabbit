# **ReportRabbit** 🐇  
*A Playwright-powered Instagram mass-reporting tool (Unstable/In Development)*  

📧 **Contact**: [report0rabbit@gmail.com](mailto:report0rabbit@gmail.com)  
⚠ **Warning**: This tool violates Instagram's Terms of Service. Use at your own risk.  

---

## **🔧 Features**  
- **Automated Instagram reporting** (Nudity/Sexual Content)  
- **Windscribe VPN integration** (IP rotation)  
- **Temporary email generation** (via [emailtm](https://emailtm.com))  
- **Playwright** for stealthy browser automation  
- **Rich** for colorful CLI output  

---

## **⚙️ Installation**  

### **Prerequisites**  
- **Python 3.10+**  
- **Windscribe VPN** (installed & logged in)  
- **Playwright browsers** (installed via CLI)  

### **Setup**  
1. Clone the repo:  
   ```bash
   git clone https://github.com/Suuuiiiiii/ReportRabbit.git && cd ReportRabbit
   ```
2. Create a virtual environment (recommended):  
   ```bash
   python -m venv venv && source venv/bin/activate  # Linux/macOS
   ```
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
4. Install Playwright browsers:  
   ```bash
   playwright install chromium
   ```

---

## **🚀 Usage**  

1. **Log in to Windscribe VPN** (required before running).  
2. Activate the virtual environment (if used):  
   ```bash
   source venv/bin/activate  # Linux/macOS
   ```
3. Run the tool:  
   ```bash
   python main.py
   ```
4. Follow the prompts:  
   - Select **Instagram** (`1`)  
   - Choose **Nudity/Sexual Exposure** (`1`)  
   - Enter **target username**  
   - Set **number of reports**  
   - Toggle **VPN (Windscribe) ON/OFF**  

---

## **🛠 How It Works**  
1. **Launches a hidden Chromium browser** (Playwright)  
2. **Generates a disposable email** (emailtm)  
3. **Creates a fake Instagram account**  
4. **Reports the target account** (Nudity)  
5. **Logs out & repeats** (with new accounts)  

---

## **⚠️ Known Issues**  
❌ **Unstable** (Email verification may fail)  
❌ **No proxy rotation** (Relies on Windscribe)  
❌ **Instagram may detect & block automation**  

---

## **📜 Legal Disclaimer**  
This tool is for **educational purposes only**. Mass reporting violates Instagram's policies. The developer (*report0rabbit@gmail.com*) is **not responsible** for misuse.  

---

## **🔮 Planned Improvements**  
✅ **Multi-threading** (Faster reporting)  
✅ **Proxy/VPN auto-switching**  
✅ **CAPTCHA bypass**  

---

### **📝 Notes**  
- **This is a work in progress!** Expect bugs.  
- **Run in a virtual environment** (`venv`) to avoid dependency conflicts.  
- **Windscribe must be running manually** (No API integration yet).  
- **If you manage to find an error or have improvements in the code please report it to report0rabbit@gmail.com** thank you.
---
