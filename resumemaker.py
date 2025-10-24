from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QCheckBox, QComboBox, QTextEdit,
    QLineEdit, QFileDialog, QPushButton, QHBoxLayout, QVBoxLayout, QButtonGroup,
    QDialog, QFormLayout, QListWidget, QListWidgetItem, QMessageBox
)
import os, sys, json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# İş Deneyimi Ekleme Penceresi
class AddJobDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("İş Deneyimi Ekle")
        layout = QFormLayout(self)

        self.start_year = QLineEdit()
        self.end_year = QLineEdit()
        self.position = QLineEdit()
        self.desc = QTextEdit()

        layout.addRow("Başlangıç Yılı:", self.start_year)
        layout.addRow("Bitiş Yılı:", self.end_year)
        layout.addRow("Pozisyon:", self.position)
        layout.addRow("Açıklama:", self.desc)

        btn_ok = QPushButton("Ekle")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def get_data(self):
        return {
            "start_year": self.start_year.text(),
            "end_year": self.end_year.text(),
            "position": self.position.text(),
            "description": self.desc.toPlainText()
        }


# Eğitim Bilgisi Ekleme Penceresi
class AddEduDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eğitim Bilgisi Ekle")
        layout = QFormLayout(self)

        self.school = QLineEdit()
        self.degree = QComboBox()
        self.degree.addItems(["Doktora", "Yüksek Lisans", "Lisans", "Önlisans", "Lise", "Ortaokul"])
        self.start_year = QLineEdit()
        self.end_year = QLineEdit()

        layout.addRow("Okul:", self.school)
        layout.addRow("Derece:", self.degree)
        layout.addRow("Başlangıç Yılı:", self.start_year)
        layout.addRow("Bitiş Yılı:", self.end_year)

        btn_ok = QPushButton("Ekle")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def get_data(self):
        return {
            "school": self.school.text(),
            "degree": self.degree.currentText(),
            "start_year": self.start_year.text(),
            "end_year": self.end_year.text()
        }


# Ana Uygulama
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Özgeçmiş Oluşturucu")
        self.setGeometry(0, 0, 900, 900)

        with open('sehirler.json', 'r', encoding="utf-8") as il:
            self.ili = json.load(il)
        with open('ilceler.json', 'r', encoding="utf-8") as ilce:
            self.ilcei = json.load(ilce)

        self.city_names = [city["sehir_adi"] for city in self.ili]
        self.job_entries = []
        self.edu_entries = []
        self.selected_image = None

        self.setup_ui()

    def setup_ui(self):
        # Genel Bilgiler
        self.isim = QLabel("İsim Soyisim:")
        self.isimtxt = QLineEdit()

        self.cinsiyet = QLabel("Cinsiyetiniz:")
        self.cinsradio1 = QRadioButton("Erkek")
        self.cinsradio2 = QRadioButton("Kadın")
        self.cins = QButtonGroup(self)
        self.cins.addButton(self.cinsradio1)
        self.cins.addButton(self.cinsradio2)

        self.il = QLabel("Şehir:")
        self.comboil = QComboBox()
        self.comboil.addItems(self.city_names)
        self.comboil.setCurrentIndex(-1)

        self.ilce = QLabel("İlçe:")
        self.comboilce = QComboBox()
        self.comboil.currentTextChanged.connect(self.ilceselect)

        self.telno = QLabel("Telefon Numarası:")
        self.notxt = QLineEdit()

        self.meslek = QLabel("Mevcut Meslek:")
        self.meslektxt = QLineEdit()

        self.özet = QLabel("Özgeçmiş Özetiniz:")
        self.özettxt = QTextEdit()

        self.job_lbl = QLabel("İş Deneyimleri:")
        self.job_add = QPushButton("Ekle")
        self.job_add.clicked.connect(self.add_job_entry)
        self.job_list = QListWidget()
        self.job_del = QPushButton("Seçileni Sil")
        self.job_del.clicked.connect(self.delete_job_entry)

        self.edu_lbl = QLabel("Eğitim Bilgileri:")
        self.edu_add = QPushButton("Ekle")
        self.edu_add.clicked.connect(self.add_edu_entry)
        self.edu_list = QListWidget()
        self.edu_del = QPushButton("Seçileni Sil")
        self.edu_del.clicked.connect(self.delete_edu_entry)
        
        self.hobi = QLabel("Hobiler:")
        self.hobicheck1 = QCheckBox("Video Oyunları")
        self.hobicheck2 = QCheckBox("Çizim/Resim")
        self.hobicheck3 = QCheckBox("Müzik")
        self.hobicheck4 = QCheckBox("Filmler/Diziler")
        self.hobicheck5 = QCheckBox("Kitap Okumak")
        self.hobicheckother = QCheckBox("Diğer")
        self.lineedithobi = QLineEdit()
        self.lineedithobi.setEnabled(False)
        self.hobicheckother.stateChanged.connect(self.addhobi_text)

        hobilayout = QHBoxLayout()
        for cb in [self.hobicheck1, self.hobicheck2, self.hobicheck3, self.hobicheck4, self.hobicheck5, self.hobicheckother]:
            hobilayout.addWidget(cb)
        hobilayout.addWidget(self.lineedithobi)

        self.dil = QLabel("İngilizce Seviyeniz:")
        self.ingsec1 = QRadioButton("Çok İyi")
        self.ingsec2 = QRadioButton("İyi")
        self.ingsec3 = QRadioButton("Orta")
        self.ingsec4 = QRadioButton("Kötü")
        self.ingsec5 = QRadioButton("Çok Kötü")
        self.seviye = QButtonGroup(self)
        for rb in [self.ingsec1, self.ingsec2, self.ingsec3, self.ingsec4, self.ingsec5]:
            self.seviye.addButton(rb)

        inglayout = QHBoxLayout()
        for rb in [self.ingsec1, self.ingsec2, self.ingsec3, self.ingsec4, self.ingsec5]:
            inglayout.addWidget(rb)

        self.photo_lbl = QLabel("Fotoğraf Seç:")
        self.photo_btn = QPushButton("Seç")
        self.photo_btn.clicked.connect(self.pick_photo)

        self.exportbtn = QPushButton("CV Oluştur (PDF)")
        self.exportbtn.clicked.connect(self.export_pdf)

        layout = QVBoxLayout()
        for w in [
            self.isim, self.isimtxt, self.cinsiyet, self.cinsradio1, self.cinsradio2,
            self.il, self.comboil, self.ilce, self.comboilce, self.telno, self.notxt,
            self.meslek, self.meslektxt, self.özet, self.özettxt,
            self.job_lbl, self.job_add, self.job_list, self.job_del,
            self.edu_lbl, self.edu_add, self.edu_list, self.edu_del,
            self.hobi
        ]:
            layout.addWidget(w)
        layout.addLayout(hobilayout)
        layout.addWidget(self.dil)
        layout.addLayout(inglayout)
        layout.addWidget(self.photo_lbl)
        layout.addWidget(self.photo_btn)
        layout.addWidget(self.exportbtn)
        self.setLayout(layout)

    def addhobi_text(self):
        self.lineedithobi.setEnabled(self.hobicheckother.isChecked())

    def ilceselect(self):
        provence_names = [p["ilce_adi"] for p in self.ilcei if p["sehir_adi"] == self.comboil.currentText()]
        self.comboilce.clear()
        self.comboilce.addItems(provence_names)

    def add_job_entry(self):
        dlg = AddJobDialog(self)
        if dlg.exec_():
            data = dlg.get_data()
            self.job_entries.append(data)
            self.job_list.addItem(f"{data['start_year']} - {data['end_year']} | {data['position']}")

    def delete_job_entry(self):
        idx = self.job_list.currentRow()
        if idx >= 0:
            self.job_list.takeItem(idx)
            del self.job_entries[idx]

    def add_edu_entry(self):
        dlg = AddEduDialog(self)
        if dlg.exec_():
            data = dlg.get_data()
            self.edu_entries.append(data)
            self.edu_list.addItem(f"{data['start_year']} - {data['end_year']} | {data['school']} ({data['degree']})")

    def delete_edu_entry(self):
        idx = self.edu_list.currentRow()
        if idx >= 0:
            self.edu_list.takeItem(idx)
            del self.edu_entries[idx]

    def pick_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.selected_image = path

    def export_pdf(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Kaydet", "", "PDF Files (*.pdf)")
        if not save_path:
            return
        if not save_path.endswith(".pdf"):
            save_path += ".pdf"

        c = canvas.Canvas(save_path)
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        c.rect(30, 30, 535, 782)
        
        if self.selected_image:
            try:
                c.drawImage(self.selected_image, 40, 680, width=120, height=130)
            except:
                c.setFont("DejaVu", 10)
                c.drawString(40, 820, "Fotoğraf yüklenemedi.")
        else:
            c.setFont("DejaVu", 10)
            c.drawString(40, 820, "Fotoğraf yok.")

        c.setFont("DejaVu", 16)
        c.drawString(220, 793, self.isimtxt.text())
        c.setFont("DejaVu", 10)
        y, x = 780, 220

        def write(text):
            nonlocal y
            c.drawString(x, y, text)
            y -= 18
        y-=7
        gender = "Erkek" if self.cinsradio1.isChecked() else ("Kadın" if self.cinsradio2.isChecked() else "")
        write("Cinsiyet: " + gender)
        write("Şehir: " + self.comboil.currentText())
        write("İlçe: " + self.comboilce.currentText())
        write("Telefon: " + self.notxt.text())
        write("Meslek: " + self.meslektxt.text())
        y -= 18
        c.line(x1=30, y1=y, x2=565, y2=y)
        
        x = 40    
        y -= 15 
        c.setFont("DejaVu", 12)
        write("Özet:")
        c.setFont("DejaVu", 10)
        for line in self.özettxt.toPlainText().split("\n"):
            write("  " + line)
        y-=18
        c.line(x1=30, y1=y, x2=565, y2=y)
        y -= 15

        c.setFont("DejaVu", 12)
        write("İş Deneyimleri:")
        c.setFont("DejaVu", 10)
        if not self.job_entries:
            write("  (Bilgi yok)")
        else:
            for job in self.job_entries:
                write(f"  {job['start_year']} - {job['end_year']} | {job['position']}")
                for line in job['description'].split("\n"):
                    write("    " + line)
        write("")
        c.line(x1=30, y1=y, x2=565, y2=y)
        y-=15
        c.setFont("DejaVu", 12)
        write("Eğitim Bilgileri:")
        c.setFont("DejaVu", 10)
        if not self.edu_entries:
            write("  (Bilgi yok)")
        else:
            for edu in self.edu_entries:
                write(f"  {edu['start_year']} - {edu['end_year']} | {edu['school']} ({edu['degree']})")
        write("")
        c.line(x1=30, y1=y, x2=565, y2=y)
        y-=15
        
        c.setFont("DejaVu", 12)
        write("Hobiler:")
        c.setFont("DejaVu", 10)
        hobbies = [cb.text() for cb in [self.hobicheck1, self.hobicheck2, self.hobicheck3, self.hobicheck4, self.hobicheck5] if cb.isChecked()]
        if self.hobicheckother.isChecked() and self.lineedithobi.text():
            hobbies.append(self.lineedithobi.text())
        write("  " + (", ".join(hobbies) if hobbies else "(Bilgi yok)"))
        write("")
        c.line(x1=30, y1=y, x2=565, y2=y)
        y-=15

        c.setFont("DejaVu", 12)
        write("İngilizce Seviyesi:")
        c.setFont("DejaVu", 10)
        levels = [("Çok İyi", self.ingsec1), ("İyi", self.ingsec2), ("Orta", self.ingsec3), ("Kötü", self.ingsec4), ("Çok Kötü", self.ingsec5)]
        level = next((lvl for lvl, rb in levels if rb.isChecked()), "(Bilgi yok)")
        write("  " + level)

        c.save()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
