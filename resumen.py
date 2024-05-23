from io import BytesIO
from PyPDF2 import PdfReader
import nltk
import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QMessageBox, QDialog, QVBoxLayout, QWidget, QPushButton,QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5 import uic
nltk.download('punkt')
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import google.generativeai as genai
from PyQt5.QtGui import QCursor


class VentanaResumen(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi('resumenia.ui', self)
        self.GOOGLE_API_KEY = 'AIzaSyCwO1BiCMbke230xVOYgfq6aIZxv_tpR20'
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.pdf_actual=""

        # Crear QScrollArea para el resumen
        self.scroll_area_resumen = QScrollArea(self)
        self.scroll_area_resumen.setWidgetResizable(True)
        self.labelResumen = QLabel(self.scroll_area_resumen)
        self.scroll_area_resumen.setWidget(self.labelResumen)
        self.verticalLayoutResumen.addWidget(self.scroll_area_resumen)

        # Crear QScrollArea para la vigencia
        self.scroll_area_vigencia = QScrollArea(self)
        self.scroll_area_vigencia.setWidgetResizable(True)
        self.labelVigencia = QLabel(self.scroll_area_vigencia)
        self.scroll_area_vigencia.setWidget(self.labelVigencia)
        self.verticalLayoutVigencia.addWidget(self.scroll_area_vigencia)

        self.botonGenerar.clicked.connect(self.cargarNuevoResumen)
        self.botonVigencia.clicked.connect(self.cargarVigencia)
        self.labelVigencia.setText("")

    def realizarResumenCargado(self, texto):
        self.labelVigencia.setText("")
        # Dividir el texto en palabras
        palabras = texto.split()
        # Unir las palabras en grupos de 10 con un salto de línea
        lineas = [' '.join(palabras[i:i+15]) for i in range(0, len(palabras), 15)]
        # Unir las líneas con saltos de línea
        wrapped_content = '\n'.join(lineas)
        self.labelResumen.setAlignment(Qt.AlignCenter)
        self.labelResumen.setText(wrapped_content)

    def cargarPDF(self,pdf):
        self.pdf_actual=pdf

    def cargarNuevoResumen(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        nuevo_resumen=self.generarResumenIA(self.pdf_actual)
        self.realizarResumenCargado(nuevo_resumen)
        QApplication.restoreOverrideCursor()
        
    def cargarVigencia(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        nueva_vigencia=self.generarVigencia(self.pdf_actual)
        self.labelVigencia.setAlignment(Qt.AlignCenter)
        self.labelVigencia.setText(nueva_vigencia)
        QApplication.restoreOverrideCursor()

    def realizarResumen(self, texto):
        response = self.model.generate_content("Necesito un mini resumen de no más de 60 palabras del siguiente convenio resaltando las partes más importantes: " + texto)
        respuesta_resumen = response.text
        wrapped_content = '\n'.join([respuesta_resumen[i:i+75] for i in range(0, len(respuesta_resumen), 75)])
        self.labelResumen.setText(wrapped_content)

        response2 = self.model.generate_content("Necesito saber la vigencia de este convenio, lo que me sirve saber es si está vencida o no y si venció cuando fue: " + texto)
        respuesta_vigencia = response2.text
        wrapped_content2 = '\n'.join([respuesta_vigencia[i:i+75] for i in range(0, len(respuesta_vigencia), 75)])
        self.labelVigencia.setText(wrapped_content2)
        
    def realizarResumenSumy(self, texto):
        wrapped_content = '\n'.join([texto[i:i+75] for i in range(0, len(texto), 75)])
        self.labelResumen.setText(wrapped_content)
        
    def generarResumenIA(self,texto):
        response = self.model.generate_content("Necesito un mini resumen de no más de 60 palabras del siguiente convenio resaltando las partes más importantes: " + texto)
        respuesta_resumen = response.text
        return respuesta_resumen
    
    def generarVigencia(self,texto):
        response = self.model.generate_content(texto+" Solo dame la fecha de vencimiento, suele estar acompañado de un sinónimo de vencimiento, necesito unicamente la fecha sin nada extra como notas, explicaciones, información adicional, etc no me des ningún otro apartado ni aclaración de que es la fecha. NECESITO LA FECHA UNICAMENTE EN FORMATO (YYYY-MMM-MMM) En caso de que no haya una fecha de vencimiento necesito que me devuelvas (NO TIENE DATOS DEL VENCIMIENTO). También teniendo en cuenta que en varías ocasiones la firma dirá que durará x cantidad de tiempo luego de la fecha inicial.")
        respuesta_resumen = response.text
        return respuesta_resumen
    
    def generar_resumen_cargado(self,texto):
        wrapped_content = '\n'.join([texto[i:i+75] for i in range(0, len(texto), 75)])
        self.labelResumen.setText(wrapped_content)
        
# Aquí deberías instanciar y mostrar la ventana  
def generar_resumen(texto, oraciones=3):
    parser = PlaintextParser.from_string(texto, Tokenizer("spanish"))
    # Using LexRank
    summarizer = LexRankSummarizer()
    # Summarize the document with 2 sentences
    summary = summarizer(parser.document, oraciones)
    # Retornar el resumen como una cadena de texto
    return " ".join([str(sentence) for sentence in summary])

def leer_pdf(linkurl):
    try:
        response = requests.get(linkurl)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        pdf_content = BytesIO(response.content)
        reader = PdfReader(pdf_content)
        number_of_pages = len(reader.pages)
        text = ''
        for i in range(number_of_pages):
            page = reader.pages[i]
            text += page.extract_text()
        
        # Muestra un mensaje indicando que la operación fue exitosa
        print("El PDF se ha leído correctamente.")
        return text
    except Exception as e:
        # Muestra un mensaje de alerta indicando que hubo un error
        print(f"Error al leer el PDF: {str(e)}")
        #arreglar lo del msgbox
        #msgbox.showinfo("Error al leer el PDF", f"Ocurrió un error al leer el pdf \n {str(e)}")
        return ""    