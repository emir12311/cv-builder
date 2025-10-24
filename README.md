# 📄 CV Builder (Özgeçmiş Oluşturucu)

This one… took real effort.  
I spent quite a while on this project — it’s not just another quick script. I made this one carefully, step by step, **for a school project**, and my teacher specifically asked for it to be **in Turkish** 🇹🇷.  

---

## ⚙️ What It Does
This app lets you create your **own CV (résumé)** with a detailed interface.  
You can enter your personal info, job experience, education, hobbies, English level, and even add your photo — then export it all as a **professional PDF**.

---

## 🪄 Features
- Add **Job Experiences** with start & end year, position, and description.  
- Add **Education Info** with school name, degree, and years.  
- Select **City and District** dynamically (based on JSON data).  
- Choose **Hobbies** or add your own custom ones.  
- Rate your **English proficiency**.  
- **Upload a photo** to include in your CV.  
- Export everything neatly into a **formatted PDF** with ReportLab.  

---

## 📦 Libraries Used
These are the **non-built-in** libraries used in this project.  
You can install them all using pip:

```bash
pip install pyqt5 reportlab
```

*(Built-in libraries used: os, sys, json)*

---

## 💡 What I Learned
- Structuring a big PyQt5 project with multiple dialog windows.  
- Dynamically updating UI elements (like the city/district system).  
- Drawing clean and organized layouts in PDFs using ReportLab.  
- Handling data with JSON and saving complex user input properly.  

---

## 🏗️ About the Project
This project isn’t just a test — it’s something I’m genuinely proud of.  
It’s one of my **most complete and polished** apps so far, showing how far I’ve come since I started learning Python.  

---

## 🗺️ Credits
- `sehirler.json` and `ilceler.json` datasets were **taken from [metinyildirimnet/turkiye-adresler-json](https://github.com/metinyildirimnet/turkiye-adresler-json)** for Turkish city and district information.  
- I only organized and used them within this project — full credit goes to the original dataset creator.  

---

## 📝 Note
This project is written **entirely in Turkish** because it was made for a **school assignment**.  
I don’t plan on rewriting or translating it right now — I want it to stay as it was when I first made it.  

Just like my other projects, I’m keeping it here to show how my skills evolve over time 🚀
