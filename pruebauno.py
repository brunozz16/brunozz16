import resumen
import webbrowser
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QStyledItemDelegate,QMainWindow, QApplication, QTableView,QHeaderView, QMessageBox, QDialog, QVBoxLayout, QWidget, QPushButton,QProgressDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QColor
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDialogButtonBox,QLabel,QMenu,QAction,QFileDialog
from PyQt5.QtCore import Qt
from datetime import datetime
import datetime
from PyQt5.QtGui import QCursor

class VentanaHistorico(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi('historico.ui', self)
        self.graficauno = Canvas_grafica_lineal()
        self.graficados = Canvas_grafica_lineal()
        self.graficatres = Canvas_grafica_lineal()
        self.tableViewAux = TableView()
        self.ventanaFilas = VentanaFilas()
        self.datouno=""
        self.datodos=""
        self.datotres=""
        self.resultado=0
        self.resultado2=0
        self.resultado3=0
        self.totaltres=[]
        self.totaldos=[]
        self.totaluno=[]
        self.años=[]
        self.filasEncontradas=[]
        self.textoGrafica1=""
        self.textoGrafica2=""
        self.textoGrafica3=""
        self.botonGrafica1.clicked.connect(self.revisarGrafica)
        self.botonGrafica2.clicked.connect(self.revisarGrafica2)
        self.botonGrafica3.clicked.connect(self.revisarGrafica3)
        self.botonFilas1.clicked.connect(lambda: self.revisarResultados(self.datouno))
        self.botonFilas2.clicked.connect(lambda: self.revisarResultados(self.datodos))
        self.botonFilas3.clicked.connect(lambda: self.revisarResultados(self.datotres))

    def revisarResultados(self,dato):
        self.filasEncontradas=[]
        current_year = datetime.datetime.now().year
        start_year = 2008
        for year in range(start_year, current_year + 1):
            anio=int(year)
            self.filasEncontradas.extend(self.tableViewAux.filtrar_datos_fecha_filas(anio,dato))
        self.ventanaFilas.setearFilas(self.filasEncontradas)
        self.ventanaFilas.setearTotal(len(self.filasEncontradas))
        self.ventanaFilas.exec_()

    def cargarGraficas(self):      
        current_year = datetime.datetime.now().year
        start_year = 2008
        for year in range(start_year, current_year + 1):
            anio=int(year)
            self.resultado=self.tableViewAux.filtrar_datos_fecha(anio,self.datouno)
            self.resultado2=self.tableViewAux.filtrar_datos_fecha(anio,self.datodos)
            self.resultado3=self.tableViewAux.filtrar_datos_fecha(anio,self.datotres)
            self.totaluno.append(self.resultado)
            self.totaldos.append(self.resultado2)
            self.totaltres.append(self.resultado3)
            self.años.append(anio)
            self.textoGrafica1+="Año "+str(anio)+" : "+str(self.resultado)+" resultados \n"
            self.textoGrafica2+="Año "+str(anio)+" : "+str(self.resultado2)+" resultados \n"
            self.textoGrafica3+="Año "+str(anio)+" : "+str(self.resultado3)+" resultados \n"
        self.resultado=self.tableViewAux.contar_datos(self.datouno)
        self.resultado2=self.tableViewAux.contar_datos(self.datodos)
        self.resultado3=self.tableViewAux.contar_datos(self.datotres)
        self.graficauno.setearValores(self.años,self.totaluno)
        self.graficauno.setearTitulo(self.datouno+" (resultados: "+str(self.resultado)+")")
        self.graficados.setearValores(self.años,self.totaldos)
        self.graficados.setearTitulo(self.datodos+" (resultados: "+str(self.resultado2)+")")
        self.graficatres.setearValores(self.años,self.totaltres)
        self.graficatres.setearTitulo(self.datotres+" (resultados: "+str(self.resultado3)+")")
        self.grafica_uno.addWidget(self.graficauno)
        self.grafica_dos.addWidget(self.graficados)
        self.grafica_tres.addWidget(self.graficatres)
        self.cargarTexto()
        
    def cargarTexto(self):
        self.textoDatos.setText(
            self.datouno+" : "+str(self.resultado)+"\n"+
            self.datodos+" : "+str(self.resultado2)+"\n"+
            self.datotres+" : "+str(self.resultado3)+"\n")

    def cargarDatos(self,d1,d2,d3):
        self.datouno=d1
        self.datodos=d2
        self.datotres=d3

    def revisarGrafica(self):
        QMessageBox.about(self, "Especifico", self.textoGrafica1)
    def revisarGrafica2(self):
        QMessageBox.about(self, "Especifico", self.textoGrafica2)
    def revisarGrafica3(self):
        QMessageBox.about(self, "Especifico", self.textoGrafica3)

    def __del__(self):
        # Método destructor, se ejecuta cuando el objeto se elimina
        self.limpiarDatos()

    def limpiarDatos(self):
        # Agrega aquí la lógica para limpiar o eliminar datos
        self.datouno = ""
        self.datodos = ""
        self.datotres = ""
        self.resultado = 0
        self.resultado2 = 0
        self.resultado3 = 0
        self.totaltres = []
        self.totaldos = []
        self.totaluno = []
        self.años = []
        self.textoGrafica1 = ""
        self.textoGrafica2 = ""
        self.textoGrafica3 = ""
        self.graficauno.limpiarGrafica()
        self.graficados.limpiarGrafica()
        self.graficatres.limpiarGrafica()    

class ResumenDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # Obtener el valor de la celda
        value = index.data()

        # Si el valor es "vacio", pintar la fila de verde
        if value == "vacio":
            painter.fillRect(option.rect, QColor(Qt.green))

        # Si no, pintar la fila de forma normal
        else:
            super().paint(painter, option, index)

# Clase para la tabla de datos
class TableView(QTableView):
    def __init__(self):
        super().__init__()
        # Aquí puedes cargar tus datos desde un archivo Excel (reemplaza 'tu_archivo.xlsx' con tu ruta de archivo)
        try:
            df = pd.read_excel('c3.xlsx')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar datos desde Excel: {str(e)}')
            return

        # Crear un modelo de tabla estándar de PyQt5
        self.model = QStandardItemModel()
        # Establecer el número de filas y columnas en el modelo
        self.model.setRowCount(df.shape[0])
        self.model.setColumnCount(df.shape[1])
        # Agregar nombres de columnas al modelo
        self.model.setHorizontalHeaderLabels(df.columns)
        self.setSelectionBehavior(QTableView.SelectRows)
        #self.resumen_column_index = 8

        # Llenar el modelo con los datos del DataFrame de pandas
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                # Formatear la columna "fecha" para mostrar solo el año-mes-día
                if df.columns[col] == 'fecha':
                    fecha_hora = df.iat[row, col]
                    if isinstance(fecha_hora, datetime):
                        fecha_truncada = fecha_hora.strftime("%Y-%m-%d")
                    else:
                        fecha_truncada = datetime.strptime(str(fecha_hora), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    item = QStandardItem(str(fecha_truncada))
                else:
                    item = QStandardItem(str(df.iat[row, col]))

                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.model.setItem(row, col, item)

        # Asignar el modelo a la QTableView
        self.setModel(self.model)
        self.doubleClicked.connect(self.mostrar_info_link)

        # Conecta la señal customContextMenuRequested a la función mostrar_menu_contextual
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        self.DialogResumen = resumen.VentanaResumen()

        #ocultar las columnas
        self.ocultar_columna_por_nombre("Doc.")
        self.ocultar_columna_por_nombre("REVISAR")
        #self.ocultar_columna_por_nombre("resumen")
        self.ocultar_columna_por_nombre("pdf")

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "resumen":
                self.resumen_column_index = col
                break

        #self.resumen_delegate = ResumenDelegate()
        #self.setItemDelegateForColumn(self.resumen_column_index, self.resumen_delegate)
        #self.cambiar_nombre_columna("numero","Número")

    def cambiar_nombre_columna(self, nombre_actual, nuevo_nombre):
        if nombre_actual not in self.model.columnNames():
            raise ValueError(f"La columna '{nombre_actual}' no existe en el modelo.")
            # Cambiar el nombre de la columna en el modelo
        self.model.setColumnHeader(self.model.getColumnIndex(nombre_actual), nuevo_nombre)
            # Actualizar la vista
        self.model.dataChanged.emit(self.model.index(0, 0), self.model.index(self.model.rowCount() - 1, self.model.columnCount() - 1))
    
    def agregar_filas(self, filas):
        for row in range(self.model.rowCount()):
            # Si la fila no está en las filas encontradas, continuar con la siguiente iteración
            if row not in filas:
                self.setRowHidden(row, True)
    
    def cargar_resumen_fila(self,index):
        # Buscar el índice de la columna "pdf"
        col_idx_pdf = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "pdf":
                col_idx_pdf = col
                break

        if col_idx_pdf == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "pdf" en la tabla.')
            return

        # Buscar el índice de la columna "resumen"
        col_idx_resumen = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "resumen":
                col_idx_resumen = col
                break

        if col_idx_resumen == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "resumen" en la tabla.')
            return

        # Llenar la columna "resumen" con el contenido de la columna "pdf"
        row = index.row()
        item_pdf = self.model.item(row, col_idx_pdf)
        item_resumen = self.model.item(row, col_idx_resumen)
        pdf = item_pdf.text()
        resumen=item_resumen.text()
        if  pdf != "vacio" and resumen == "vacio":
            print("entra:"+pdf)
            #resumen_valor ="tiene"
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            resumen_valor = self.DialogResumen.generarResumenIA(pdf)
            # Crear un nuevo item y establecer el texto
            item_pdf = QStandardItem(resumen_valor)
            item_pdf.setFlags(item_pdf.flags() ^ Qt.ItemIsEditable)
            
            # Asignar el nuevo item a la columna "resumen"
            self.model.setItem(row, col_idx_resumen, item_pdf)
            QApplication.restoreOverrideCursor()

    def cargar_resumen(self):
        # Buscar el índice de la columna "pdf"
        col_idx_pdf = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "pdf":
                col_idx_pdf = col
                break

        if col_idx_pdf == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "pdf" en la tabla.')
            return

        # Buscar el índice de la columna "resumen"
        col_idx_resumen = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "resumen":
                col_idx_resumen = col
                break

        if col_idx_resumen == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "resumen" en la tabla.')
            return

        # Llenar la columna "resumen" con el contenido de la columna "pdf"
        for row in range(self.model.rowCount()):
            item_pdf = self.model.item(row, col_idx_pdf)
            item_resumen = self.model.item(row, col_idx_resumen)
            pdf = item_pdf.text()
            resumen=item_resumen.text()
            if  pdf != "vacio" and resumen == "vacio":
                #resumen_valor ="tiene"
                resumen_valor = self.DialogResumen.generarResumenIA(pdf)
                # Crear un nuevo item y establecer el texto
                item_pdf = QStandardItem(resumen_valor)
                item_pdf.setFlags(item_pdf.flags() ^ Qt.ItemIsEditable)
            
                # Asignar el nuevo item a la columna "resumen"
                self.model.setItem(row, col_idx_resumen, item_pdf)
    
    def cargar_pdf_fila(self,index):
        # Buscar el índice de la columna "link"
        col_idx_numero = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "enlace":
                col_idx_numero = col
                break

        if col_idx_numero == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "numero" en la tabla.')
            return

        # Buscar el índice de la columna "pdf"
        col_idx_pdf = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "pdf":
                col_idx_pdf = col
                break

        if col_idx_pdf == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "pdf" en la tabla.')
            return

        # Llenar la columna "pdf-" con el contenido de la columna "numero"
        row = index.row()
        item_numero = self.model.item(row, col_idx_numero)
        numero = item_numero.text()
        print(numero)
        valorpdf=resumen.leer_pdf(numero)
        #print(valorpdf)

        if valorpdf != "":
            pdf_valor = valorpdf
        else:
            pdf_valor ="vacio"

        # Crear un nuevo item y establecer el texto
        item_pdf = QStandardItem(pdf_valor)
        item_pdf.setFlags(item_pdf.flags() ^ Qt.ItemIsEditable)
            
        # Asignar el nuevo item a la columna "pdf"
        self.model.setItem(row, col_idx_pdf, item_pdf)
    
    def cargar_pdf(self):
        # Buscar el índice de la columna "link"
        col_idx_numero = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "enlace":
                col_idx_numero = col
                break

        if col_idx_numero == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "numero" en la tabla.')
            return

        # Buscar el índice de la columna "pdf"
        col_idx_pdf = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "pdf":
                col_idx_pdf = col
                break

        if col_idx_pdf == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "pdf" en la tabla.')
            return

        # Llenar la columna "pdf" con el contenido de la columna "numero"
        for row in range(self.model.rowCount()):
            item_numero = self.model.item(row, col_idx_numero)
            numero = item_numero.text()
            if resumen.leer_pdf(numero) != "":
                pdf_valor = resumen.leer_pdf(numero)
            else:
                pdf_valor ="vacio"

            # Crear un nuevo item y establecer el texto
            item_pdf = QStandardItem(pdf_valor)
            item_pdf.setFlags(item_pdf.flags() ^ Qt.ItemIsEditable)
            
            # Asignar el nuevo item a la columna "pdf"
            self.model.setItem(row, col_idx_pdf, item_pdf)
            
            #llamamos a generar resumen
            #self.cargar_resumen()

    def buscar_descripcion_y_anio(self, texto_filtro):
        # Buscar el índice de la columna "descripcion"
        col_idx_descripcion = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "descripción":
                col_idx_descripcion = col
                break

        if col_idx_descripcion == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "descripcion" en la tabla.')
            return

        # Buscar el índice de la columna "fecha"
        col_idx_fecha = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "fecha":
                col_idx_fecha = col
                break

        if col_idx_fecha == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "fecha" en la tabla.')
            return

        # Contadores para el número de resultados encontrados
        resultados_descripcion = 0
        resultados_anio = 0

        # Obtener las palabras clave de los filtros separados por coma
        palabras_clave = [palabra.strip().lower() for palabra in texto_filtro.split(',')]

        # Obtener el año del plain text edit
        try:
            año_filtro = int(self.labelDescripcionFecha.toPlainText().strip())
        except ValueError:
            QMessageBox.warning(self, 'Advertencia', 'Ingrese un año válido.')
            return

        # Filtrar los datos según el texto ingresado en la columna "descripcion"
        for row in range(self.model.rowCount()):
            item_descripcion = self.model.item(row, col_idx_descripcion)
            descripcion = item_descripcion.text().lower()

            # Verificar si al menos una palabra clave está presente en la descripción
            alguna_palabra_clave_presente = any(palabra in descripcion for palabra in palabras_clave)

            # Mostrar la fila si al menos una palabra clave está presente
            if alguna_palabra_clave_presente:
                self.setRowHidden(row, False)
                resultados_descripcion += 1
            else:
                self.setRowHidden(row, True)

        # Filtrar los datos según el año ingresado en la columna "fecha"
        for row in range(self.model.rowCount()):
            item_fecha = self.model.item(row, col_idx_fecha)
            fecha_fila = item_fecha.text() if item_fecha else ""

            # Verificar si el año coincide
            año_coincide = self.año_coincide(fecha_fila, año_filtro)

            # Mostrar la fila si el año coincide
            if año_coincide:
                self.setRowHidden(row, False)
                resultados_anio += 1

        # Mostrar notificación con el número de resultados encontrados
        QMessageBox.information(self, 'Resultados encontrados', f'Se encontraron {resultados_descripcion} resultados por descripción y {resultados_anio} resultados por año.')

    def año_coincide(self, fecha_str, año):
    # Verificar si el año en la fecha coincide con el año proporcionado
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha.year == año
        except ValueError:
            return False

    def filtrar_datos_or_2(self, texto_filtro):
        # Buscar el índice de la columna "descripcion"
        col_idx = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "descripción":
                col_idx = col
                break

        if col_idx == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "descripcion" en la tabla.')
            return
        
        # Contador para el número de resultados encontrados
        resultados_encontrados = 0

        # Obtener las palabras clave de los filtros separados por coma
        palabras_clave = [palabra.strip().lower() for palabra in texto_filtro.split(',')]
        # Lista para almacenar los índices de las filas que cumplen con el criterio de búsqueda
        filas_encontradas = []

        # Filtrar los datos según el texto ingresado en la columna "descripcion"
        for row in range(self.model.rowCount()):
            item = self.model.item(row, col_idx)
            descripcion = item.text().lower()

            # Verificar si al menos una palabra clave está presente en la descripción
            alguna_palabra_clave_presente = any(palabra in descripcion for palabra in palabras_clave)

            if alguna_palabra_clave_presente:
                # Almacenar el índice de la fila si al menos una palabra clave está presente
                filas_encontradas.append(row)
                resultados_encontrados += 1
                # No es necesario cambiar la visibilidad de la fila aquí

        # Retornar la lista de índices de filas encontradas
        return filas_encontradas

    def filtrar_datos_fecha(self, año, texto_filtro):
        filas_encontradas=self.filtrar_datos_and(texto_filtro)
        # Validar que el texto sea un año válido (puedes realizar una validación más robusta según tus necesidades)
        if not str(año).isdigit() or len(str(año)) != 4:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese un año válido (formato: YYYY).')
            return

        # Convertir el año a entero
        anio = int(año)
        resultados_encontrados=0

        # Buscar el índice de la columna "fecha"
        col_idx_fecha = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "fecha":
                col_idx_fecha = col
                break

        if col_idx_fecha == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "fecha" en la tabla.')
            return

        # Filtrar los datos según el año ingresado en la columna "fecha" y las filas encontradas
        for row in range(self.model.rowCount()):
            # Si la fila no está en las filas encontradas, continuar con la siguiente iteración
            if row not in filas_encontradas:
                continue

            item = self.model.item(row, col_idx_fecha)
            fecha_hora = str(item.text())
            fecha_anio = int(fecha_hora[:4]) if len(fecha_hora) >= 4 else None

            if fecha_anio == anio:
                # Mostrar la fila si el año coincide
                #self.setRowHidden(row, False)
                resultados_encontrados+=1
            #else:
                # Ocultar la fila si el año no coincide
                #self.setRowHidden(row, True)
        
        return resultados_encontrados
                
        # Mostrar notificación con el número de resultados encontrados
        #QMessageBox.information(self, 'Resultados encontrados', f'Se encontraron {resultados_encontrados} resultados.')

    def filtrar_datos_fecha_filas(self, año, texto_filtro):
        filas_encontradas=self.filtrar_datos_and(texto_filtro)
        # Validar que el texto sea un año válido (puedes realizar una validación más robusta según tus necesidades)
        filas=[]
        if not str(año).isdigit() or len(str(año)) != 4:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese un año válido (formato: YYYY).')
            return

        # Convertir el año a entero
        anio = int(año)
        resultados_encontrados=0

        # Buscar el índice de la columna "fecha"
        col_idx_fecha = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "fecha":
                col_idx_fecha = col
                break

        if col_idx_fecha == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "fecha" en la tabla.')
            return

        # Filtrar los datos según el año ingresado en la columna "fecha" y las filas encontradas
        for row in range(self.model.rowCount()):
            # Si la fila no está en las filas encontradas, continuar con la siguiente iteración
            if row not in filas_encontradas:
                continue

            item = self.model.item(row, col_idx_fecha)
            fecha_hora = str(item.text())
            fecha_anio = int(fecha_hora[:4]) if len(fecha_hora) >= 4 else None

            if fecha_anio == anio:
                filas.append(row)
                
        return filas

    def buscar_por_anio_2(self, año, filas_encontradas):
        # Validar que el texto sea un año válido (puedes realizar una validación más robusta según tus necesidades)
        if not año.isdigit() or len(año) != 4:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese un año válido (formato: YYYY).')
            return

        # Convertir el año a entero
        anio = int(año)
        resultados_encontrados=0

        # Buscar el índice de la columna "fecha"
        col_idx_fecha = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "fecha":
                col_idx_fecha = col
                break

        if col_idx_fecha == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "fecha" en la tabla.')
            return

        # Filtrar los datos según el año ingresado en la columna "fecha" y las filas encontradas
        for row in range(self.model.rowCount()):
            # Si la fila no está en las filas encontradas, continuar con la siguiente iteración
            if row not in filas_encontradas:
                continue

            item = self.model.item(row, col_idx_fecha)
            fecha_hora = str(item.text())
            fecha_anio = int(fecha_hora[:4]) if len(fecha_hora) >= 4 else None

            if fecha_anio == anio:
                # Mostrar la fila si el año coincide
                self.setRowHidden(row, False)
                resultados_encontrados+=1
            else:
                # Ocultar la fila si el año no coincide
                self.setRowHidden(row, True)
           
                
        # Mostrar notificación con el número de resultados encontrados
        QMessageBox.information(self, 'Resultados encontrados', f'Se encontraron {resultados_encontrados} resultados.')

    def filtrar_or(self,texto_filtro,año):
        if len(año)>0:
            # Llamada a la función filtrar_datos_or
            filas_encontradas = self.filtrar_datos_or_2(texto_filtro)
            # Llamada a la función buscar_por_anio
            self.buscar_por_anio_2(año, filas_encontradas)
        else:
            self.filtrar_datos_or(texto_filtro)

    def filtrar_and(self,texto_filtro,año):
        if len(año)>0:
            # Llamada a la función filtrar_datos_or
            filas_encontradas = self.filtrar_datos_and(texto_filtro)
            # Llamada a la función buscar_por_anio
            self.buscar_por_anio_2(año, filas_encontradas)
        else:
            self.filtrar_datos_and_2(texto_filtro)
    
    def filtrar_datos_or(self, texto_filtro):
        # Buscar el índice de la columna "descripcion"
        col_idx = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "descripción":
                col_idx = col
                break

        if col_idx == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "descripcion" en la tabla.')
            return
        
        # Contador para el número de resultados encontrados
        resultados_encontrados = 0

        # Obtener las palabras clave de los filtros separados por coma
        palabras_clave = [palabra.strip().lower() for palabra in texto_filtro.split(',')]

        # Filtrar los datos según el texto ingresado en la columna "descripcion"
        for row in range(self.model.rowCount()):
            item = self.model.item(row, col_idx)
            descripcion = item.text().lower()

            # Verificar si al menos una palabra clave está presente en la descripción
            alguna_palabra_clave_presente = any(palabra in descripcion for palabra in palabras_clave)

            if alguna_palabra_clave_presente:
                # Mostrar la fila si al menos una palabra clave está presente
                self.setRowHidden(row, False)
                resultados_encontrados += 1
            else:
                # Ocultar la fila si ninguna palabra clave está presente
                self.setRowHidden(row, True)

        # Mostrar notificación con el número de resultados encontrados
        QMessageBox.information(self, 'Resultados encontrados', f'Se encontraron {resultados_encontrados} resultados.')

    def filtrar_datos_and(self, texto_filtro):
        # Buscar el índice de la columna "descripcion"
        col_idx = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "descripción":
                col_idx = col
                break
            
        col_idx_pdf = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "pdf":
                col_idx_pdf = col
                break

        if col_idx == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "descripcion" en la tabla.')
            return []

        # Lista para almacenar las filas encontradas
        filas_encontradas = []

        # Obtener las palabras clave de los filtros separados por coma
        palabras_clave = [palabra.strip().lower() for palabra in texto_filtro.split(',')]

        # Filtrar los datos según el texto ingresado en la columna "descripcion"
        for row in range(self.model.rowCount()):
            item = self.model.item(row, col_idx)
            item2 = self.model.item(row, col_idx_pdf)
            descripcion = item.text().lower()
            pdf=item2.text().lower()
            descripcion=descripcion+" "+pdf
            # Verificar si todas las palabras clave están presentes en la descripción
            todas_palabras_clave_presentes = all(palabra in descripcion for palabra in palabras_clave)

            if todas_palabras_clave_presentes:
                # Agregar la fila a la lista de filas encontradas
                filas_encontradas.append(row)

        # Retornar la lista de filas encontradas
        return filas_encontradas

    def filtrar_datos_and_2(self, texto_filtro):
            # Buscar el índice de la columna "descripcion"
            col_idx = -1
            for col in range(self.model.columnCount()):
                if self.model.horizontalHeaderItem(col).text().lower() == "descripción":
                    col_idx = col
                    break
                
            col_idx_pdf = -1
            for col in range(self.model.columnCount()):
                if self.model.horizontalHeaderItem(col).text().lower() == "pdf":
                    col_idx_pdf = col
                    break

            if col_idx == -1:
                QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "descripcion" en la tabla.')
                return

            # Contador para el número de resultados encontrados
            resultados_encontrados = 0

            # Obtener las palabras clave de los filtros separados por coma
            palabras_clave = [palabra.strip().lower() for palabra in texto_filtro.split(',')]

            # Filtrar los datos según el texto ingresado en la columna "descripcion"
            for row in range(self.model.rowCount()):
                item = self.model.item(row, col_idx)
                item2 = self.model.item(row, col_idx_pdf)
                descripcion = item.text().lower()
                pdf=item2.text().lower()
                descripcion=descripcion+" "+pdf
                # Verificar si todas las palabras clave están presentes en la descripción
                todas_palabras_clave_presentes = all(palabra in descripcion for palabra in palabras_clave)

                if todas_palabras_clave_presentes:
                    # Mostrar la fila si todas las palabras clave están presentes
                    self.setRowHidden(row, False)
                    resultados_encontrados += 1
                else:
                    # Ocultar la fila si alguna palabra clave no está presente
                    self.setRowHidden(row, True)

            # Mostrar notificación con el número de resultados encontrados
            QMessageBox.information(self, 'Resultados encontrados', f'Se encontraron {resultados_encontrados} resultados.')

    def contar_datos(self,dato):
        filas=self.filtrar_datos_and(dato)        
        return len(filas)

    def abrir_ventana_emergente(self, index):
        # Obtiene el dato enlazado al índice de la celda seleccionada
        dato = self.model.itemFromIndex(index).text()

        # Crea una ventana emergente
        ventana_emergente = QDialog(self)
        ventana_emergente.setWindowTitle('Dato en Enlace')
        layout = QVBoxLayout(ventana_emergente)
        label_dato = QLabel(f'Dato: {dato}', ventana_emergente)
        layout.addWidget(label_dato)

        # Botón para cerrar la ventana emergente
        button_box = QDialogButtonBox(QDialogButtonBox.Ok, ventana_emergente)
        button_box.accepted.connect(ventana_emergente.accept)
        layout.addWidget(button_box)

        # Muestra la ventana emergente
        ventana_emergente.exec_()

    def mostrar_info_link(self, index):
        # Obtiene el valor de la columna "link" para la fila seleccionada
        row = index.row()
        col_idx_link = 2  # Índice de la última columna (suponiendo que "link" es la última columna)
        link_value = self.model.item(row, col_idx_link).text()

        # Crea una ventana emergente para mostrar la información del link
        ventana_emergente = QDialog(self)
        ventana_emergente.setWindowTitle('Información de la descripción')
        layout = QVBoxLayout(ventana_emergente)
        label_info = QLabel(f' {link_value}', ventana_emergente)
        layout.addWidget(label_info)

        # Botón para cerrar la ventana emergente
        button_box = QDialogButtonBox(QDialogButtonBox.Ok, ventana_emergente)
        button_box.accepted.connect(ventana_emergente.accept)
        layout.addWidget(button_box)

        # Muestra la ventana emergente
        ventana_emergente.exec_()

    def mostrar_info_link_click_derecho(self, index):
        # Obtiene el valor de la columna "link" para la fila seleccionada
        row = index.row()
        #col_idx_link = self.model.columnCount() - 1  # Índice de la última columna (suponiendo que "link" es la última columna)
        
        col_idx_link = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "enlace":
                col_idx_link = col
                break
        
        
        link_value = self.model.item(row, col_idx_link).text()

        # Verifica si la URL es válida antes de abrir el navegador
        if link_value:
            try:
                # Intenta abrir la URL en el navegador web predeterminado
                webbrowser.open(link_value)
            except Exception as e:
                # Muestra una ventana emergente si hay un error al abrir la URL
                QMessageBox.warning(self, 'Error al abrir la URL', f'Error: {str(e)}')
        else:
            # Muestra un mensaje si no hay valor en la columna "link"
            QMessageBox.warning(self, 'Sin URL', 'No hay URL disponible para esta fila.')

    def mostrar_menu_contextual(self, pos):
        # Crea un menú contextual al hacer clic derecho
        menu = QMenu(self)
        abrir_link_action = menu.addAction('Abrir PDF del convenio')
        abrir_link_action.triggered.connect(lambda: self.abrir_link_desde_menu_contextual(opcion=1))
        
        # Acción adicional 1
        accion_adicional_1 = QAction('Abrir datos del convenio', self)
        accion_adicional_1.triggered.connect(lambda: self.abrir_link_desde_menu_contextual(opcion=2))
        menu.addAction(accion_adicional_1)

        # Acción adicional 2
        #accion_adicional_2 = QAction('Abrir resumen del convenio(Sumy)', self)
        #accion_adicional_2.triggered.connect(lambda: self.abrir_link_desde_menu_contextual(opcion=3))
        #menu.addAction(accion_adicional_2)
        
        # Acción adicional 3
        accion_adicional_3 = QAction('Abrir resumen del convenio(IA)', self)
        accion_adicional_3.triggered.connect(lambda: self.abrir_link_desde_menu_contextual(opcion=4))
        menu.addAction(accion_adicional_3)

        # Acción adicional 4
        accion_adicional_4 = QAction('Cargar pdf y resumen', self)
        accion_adicional_4.triggered.connect(lambda: self.abrir_link_desde_menu_contextual(opcion=5))
        menu.addAction(accion_adicional_4)
        # Acción adicional 4
        accion_adicional_5 = QAction('Cargar resumen', self)
        accion_adicional_5.triggered.connect(lambda: self.abrir_link_desde_menu_contextual(opcion=6))
        menu.addAction(accion_adicional_5)
        
        # Muestra el menú en la posición del clic derecho
        menu.exec_(self.mapToGlobal(pos))

    def abrir_link_desde_menu_contextual(self, opcion):
    # Obtiene el índice de la celda seleccionada
        index = self.currentIndex()
        print(index)
        
        if opcion == 1:
            # Llama a la función para abrir la URL correspondiente
            self.mostrar_info_link_click_derecho(index)               
        if opcion == 2:
            # Llama a la función para abrir la URL correspondiente
            self.mostrar_info_link(index)
        if opcion == 3:
        # Llama a la función para abrir la URL correspondiente
            self.ver_resumen_sumy(index)
        # Muestra el diálogo con el resumen
            self.DialogResumen.exec_()
        if opcion == 4:
        # Muestra el indicador de carga
            progress_dialog = QProgressDialog("Cargando resumen...", None, 0, 0, self)
            progress_dialog.setWindowModality(2)  # Hace que el diálogo sea modal
            progress_dialog.show()
        # Llama a la función para ver el resumen
            self.ver_resumen_ia(index)
        # Cierra el indicador de carga después de completar la tarea
            progress_dialog.close()
            self.DialogResumen.cargarPDF(self.ver_PDF(index))
        # Muestra el diálogo con el resumen
            self.DialogResumen.exec_()

        if opcion == 5:
            self.cargar_pdf_fila(index)
            #self.cargar_resumen_fila(index)
        if opcion == 6:
            self.cargar_resumen_fila(index)
    
    def ver_PDF(self,index):
        row = index.row()
        col_idx_resumen = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "pdf":
                col_idx_resumen = col
                break
        #col_idx_link = self.model.columnCount() - 1  # Índice de la última columna (suponiendo que "link" es la última columna)
        pdf_valor = self.model.item(row, col_idx_resumen).text()
        return pdf_valor

    def ver_resumen_ia(self, index):
        row = index.row()
        col_idx_resumen = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "resumen":
                col_idx_resumen = col
                break
        #col_idx_link = self.model.columnCount() - 1  # Índice de la última columna (suponiendo que "link" es la última columna)
        link_value = self.model.item(row, col_idx_resumen).text()
        # Realiza el resumen en segundo plano
        #texto_plano_convenio = resumen.leer_pdf(link_value)
        # Asigna el resultado al diálogo de resumen
        #self.DialogResumen.realizarResumen(texto_plano_convenio)
        self.DialogResumen.realizarResumenCargado(link_value) 
        
    def ver_resumen_sumy(self,index):
        row = index.row()
        col_idx_link = self.model.columnCount() - 1  # Índice de la última columna (suponiendo que "link" es la última columna)
        link_value = self.model.item(row, col_idx_link).text()
        texto_plano_convenio=resumen.leer_pdf(link_value)
        texto_resumen=resumen.generar_resumen(texto_plano_convenio)
        print(texto_resumen)
        self.DialogResumen.realizarResumenSumy(texto_resumen) 

    def buscar_por_anio(self,año):
        # Obtener el texto del QPlainTextEdit labelFecha
        #texto_filtro = self.labelFecha.toPlainText().strip()

        # Validar que el texto sea un año válido (puedes realizar una validación más robusta según tus necesidades)
        if not año.isdigit() or len(año) != 4:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese un año válido (formato: YYYY).')
            return

        # Convertir el año a entero
        anio = int(año)

        # Buscar el índice de la columna "fecha"
        col_idx_fecha = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "fecha":
                col_idx_fecha = col
                break

        if col_idx_fecha == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "fecha" en la tabla.')
            return

        # Filtrar los datos según el año ingresado en la columna "fecha"
        for row in range(self.model.rowCount()):
            item = self.model.item(row, col_idx_fecha)
            fecha_hora = str(item.text())
            fecha_anio = int(fecha_hora[:4]) if len(fecha_hora) >= 4 else None

            if fecha_anio == anio:
                # Mostrar la fila si el año coincide
                self.setRowHidden(row, False)
            else:
                # Ocultar la fila si el año no coincide
                self.setRowHidden(row, True)

    def buscar_por_numero(self,texto_filtro):
        # Buscar el índice de la columna "descripcion"
        col_idx = -1
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text().lower() == "número":
                col_idx = col
                break

        if col_idx == -1:
            QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "numero" en la tabla.')
            return

        # Contador para el número de resultados encontrados
        resultados_encontrados = 0

        # Filtrar los datos según el texto ingresado en la columna "descripcion"
        for row in range(self.model.rowCount()):
            item = self.model.item(row, col_idx)
            if texto_filtro in item.text().lower():
                # Mostrar la fila si el texto está contenido en el elemento
                self.setRowHidden(row, False)
                resultados_encontrados += 1
            else:
                # Ocultar la fila si el texto no está contenido en el elemento
                self.setRowHidden(row, True)

        # Mostrar notificación con el número de resultados encontrados
        QMessageBox.information(self, 'Resultados encontrados', f'Se encontraron {resultados_encontrados} resultados.')

    def guardar_datos_visibles(self):
    # Crear una lista vacía para almacenar las filas
        filas = []

    # Recorrer todas las filas y columnas de la tabla
        for row in range(self.model.rowCount()):
        # Si la fila está oculta, no la incluyas en la lista
            if self.isRowHidden(row):
                continue

        # Crear un diccionario para almacenar los datos de la fila
            fila = {}
            for col in range(self.model.columnCount()):
            # Obtener el nombre de la columna
                nombre_columna = self.model.horizontalHeaderItem(col).text()
            # Obtener el valor de la celda
                valor_celda = self.model.item(row, col).text()
            # Agregar el valor de la celda al diccionario de la fila
                fila[nombre_columna] = valor_celda

        # Agregar la fila a la lista
            filas.append(fila)

    # Convertir la lista de filas en un DataFrame
        df = pd.DataFrame(filas)

    # Abrir un cuadro de diálogo para seleccionar archivos y obtener la ruta del archivo seleccionado
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar datos", "", "Excel Files (*.xlsx)")

    # Si el usuario seleccionó un archivo, guardar el DataFrame en ese archivo
        if ruta_archivo:
            df.to_excel(ruta_archivo, index=False)
    
    def filtrar(self, texto_filtro):
            # Buscar el índice de la columna "descripcion"
            col_idx = -1
            for col in range(self.model.columnCount()):
                if self.model.horizontalHeaderItem(col).text().lower() == "descripción":
                    col_idx = col
                    break
                
            col_idx_pdf = -1
            for col in range(self.model.columnCount()):
                if self.model.horizontalHeaderItem(col).text().lower() == "pdf":
                    col_idx_pdf = col
                    break

            if col_idx == -1:
                QMessageBox.warning(self, 'Advertencia', 'No se encontró la columna "descripcion" en la tabla.')
                return

            # Contador para el número de resultados encontrados
            resultados_encontrados = 0

            # Obtener las palabras clave de los filtros separados por coma
            palabras_clave = [palabra.strip().lower() for palabra in texto_filtro.split(',')]

            # Filtrar los datos según el texto ingresado en la columna "descripcion"
            for row in range(self.model.rowCount()):
                item = self.model.item(row, col_idx)
                item2 = self.model.item(row, col_idx_pdf)
                descripcion = item.text().lower()
                pdf=item2.text().lower()
                descripcion=descripcion+" "+pdf
                # Verificar si todas las palabras clave están presentes en la descripción
                todas_palabras_clave_presentes = all(palabra in descripcion for palabra in palabras_clave)

                if todas_palabras_clave_presentes:
                    # Mostrar la fila si todas las palabras clave están presentes
                    self.setRowHidden(row, False)
                    resultados_encontrados += 1
                else:
                    # Ocultar la fila si alguna palabra clave no está presente
                    self.setRowHidden(row, True)

    def limpiar_tabla(self):
        self.filtrar("")

    def ocultar_columna_por_nombre(self, nombre_columna):
       # Buscar el índice de la columna por su nombre
        for col in range(self.model.columnCount()):
            if self.model.horizontalHeaderItem(col).text() == nombre_columna:
                self.setColumnHidden(col, True)
                return

        # Si no se encuentra la columna, mostrar un mensaje de advertencia
        QMessageBox.warning(self, 'Advertencia', f'No se encontró la columna "{nombre_columna}" en la tabla.')

# Clase base para la ventana graficos
class VentanaGraficos(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi('graficos.ui', self)
        self.grafica = Canvas_grafica()
        self.grafica2 = Canvas_grafica_torta()
        self.tableViewAux = TableView()
        self.DialogHistorico = VentanaHistorico()
        self.botonCargar.clicked.connect(self.setearDatos)
        self.botonLimpiar.clicked.connect(self.limpiarGraficas)
        self.botonHistorico.clicked.connect(self.abrirHistorico)
    
    def abrirHistorico(self):
        self.DialogHistorico.limpiarDatos()
        texto_filtro_uno = self.labelCampoUno.toPlainText().lower()
        texto_filtro_dos = self.labelCampoDos.toPlainText().lower()
        texto_filtro_tres = self.labelCampoTres.toPlainText().lower()
        self.DialogHistorico.cargarDatos(texto_filtro_uno,texto_filtro_dos,texto_filtro_tres)
        self.DialogHistorico.cargarGraficas()
        self.DialogHistorico.showMaximized()
        self.close()
        self.DialogHistorico.exec_()
        
    def limpiarGraficas(self):
        self.grafica.limpiarGrafica()
        self.grafica2.limpiarGrafica()
        self.labelCampoUno.clear()
        self.labelCampoDos.clear()
        self.labelCampoTres.clear()
        self.labelDatos.setText("")

    def setearDatos(self):
        texto_filtro_uno = self.labelCampoUno.toPlainText().lower()
        texto_filtro_dos = self.labelCampoDos.toPlainText().lower()
        texto_filtro_tres = self.labelCampoTres.toPlainText().lower()
        dato_uno=self.tableViewAux.contar_datos(texto_filtro_uno)
        dato_dos=self.tableViewAux.contar_datos(texto_filtro_dos)
        dato_tres=self.tableViewAux.contar_datos(texto_filtro_tres)
        self.labelDatos.setText(texto_filtro_uno+" : "+str(dato_uno)+"\n"+
                                texto_filtro_dos+" : "+str(dato_dos)+"\n"+
                                texto_filtro_tres+" : "+str(dato_tres)+"\n")
        self.grafica_uno.addWidget(self.grafica)
        self.grafica_dos.addWidget(self.grafica2)
        self.grafica.setearValores(texto_filtro_uno,texto_filtro_dos,texto_filtro_tres,dato_uno,dato_dos,dato_tres)
        self.grafica2.setearValores(texto_filtro_uno,texto_filtro_dos,texto_filtro_tres,dato_uno,dato_dos,dato_tres)

class Canvas_grafica_lineal(FigureCanvas):
  
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(5, 5), sharey=True, facecolor='white')
        super().__init__(self.fig)

    def limpiarGrafica(self):
        self.ax.cla()
        self.draw()
        
    def setearValores(self, nombres, tamaños):
        self.limpiarGrafica()
        colores = ['#7a31b0', '#dc225a', '#ff9132']
        self.ax.plot(nombres, tamaños, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
        self.ax.set_xlabel('Años')
        self.ax.set_ylabel('Convenios cargados')
        self.ax.grid(True)
        #self.ax.set_title('Grafica Lineal')
        self.draw()
        
    def setearTitulo(self,dato):
        self.ax.set_title(dato)

class Canvas_grafica(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(5, 5), sharey=True, facecolor='white')
        super().__init__(self.fig)
        self.fig.suptitle('Grafica de Barras', size=9)

    def limpiarGrafica(self):
        self.ax.cla()
        self.draw()
        
    def setearValores(self,nom1,nom2,nom3,tam1,tam2,tam3):
        self.limpiarGrafica()
        nombres = [nom1,nom2,nom3]
        tamaño = [tam1, tam2, tam3]
        colores = ['#7a31b0','#dc225a','#ff9132']
        self.ax.bar(nombres,tamaño,color=colores)
        self.draw()

class Canvas_grafica_torta(FigureCanvas):
  
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(5, 5), sharey=True, facecolor='white')
        super().__init__(self.fig)
        self.fig.suptitle('Grafica de Torta', size=9)

    def limpiarGrafica(self):
        self.ax.cla()
        self.draw()
        
    def setearValores(self, nom1, nom2, nom3, tam1, tam2, tam3):
        self.limpiarGrafica()
        nombres = [nom1, nom2, nom3]
        tamaños = [tam1, tam2, tam3]
        colores = ['#7a31b0', '#dc225a', '#ff9132']  # Puedes cambiar los colores según tu preferencia
        self.ax.pie(tamaños, labels=nombres, autopct='%1.1f%%', colors=colores, startangle=90)
        self.ax.axis('equal')  # Hace que el gráfico de torta se vea como un círculo
        self.draw()

# Clase base para la ventana principal
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self) 
    
        self.DialogGrafico = VentanaGraficos()
        # Crear la instancia de TableView y agregarla al layout
        self.tableView = TableView()
        self.layoutTableView.addWidget(self.tableView)
        # Conecta el botón a la función de filtro
        self.botonDescripcion.clicked.connect(self.filtrar_datos)
        self.botonFecha.clicked.connect(self.filtrar_fecha)
        self.botonNumero.clicked.connect(self.filtrar_numero)
        # Llama directamente a la función mostrar al inicializar la aplicación
        self.botonGraficos.clicked.connect(self.abrir_ventana_estadisticas)
        self.botonGuardar.clicked.connect(self.tableView.guardar_datos_visibles)
        self.botonLimpiar.clicked.connect(self.tableView.limpiar_tabla)
        self.botonInstrucciones.clicked.connect(self.tableView.cargar_pdf)
        self.botonResumen.clicked.connect(self.tableView.cargar_resumen)

    def filtrar_fecha(self):
        # Obtener el texto del QPlainTextEdit
        texto_filtro = self.labelFecha.toPlainText().lower()
        # Llamar a la función filtrar_datos en la instancia de TableView
        self.tableView.buscar_por_anio(texto_filtro)
        
    def filtrar_numero(self):
        # Obtener el texto del QPlainTextEdit
        texto_filtro = self.labelNumero.toPlainText().lower()
        # Llamar a la función filtrar_datos en la instancia de TableView
        self.tableView.buscar_por_numero(texto_filtro)    

    def filtrar_datos(self):
        # Obtener el texto del QPlainTextEdit
        texto_filtro = self.labelDescripcion.toPlainText().lower()
        texto_año = self.labelDescripcionFecha.toPlainText().lower()
        # Llamar a la función filtrar_datos en la instancia de TableView
        
        textobox = self.comboBox.currentText()
        
        if textobox=="Criterio y":
            self.tableView.filtrar_and(texto_filtro,texto_año)
        else:
            self.tableView.filtrar_or(texto_filtro,texto_año)

    def abrir_ventana_estadisticas(self):
        # Crea e muestra la instancia de la ventana de estadísticas
        self.DialogGrafico.limpiarGraficas()
        self.DialogGrafico.exec_()

class VentanaFilas(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi('ventanaencontradas.ui', self)
        self.tableViewAux = TableView()
        self.layoutTabla.addWidget(self.tableViewAux)
        self.totalEncontrado=0
        self.botonDescargar.clicked.connect(self.descargarResultados)

    def setearTotal(self,total):
        self.totalEncontrado=total
        self.labelResultados.setText("Resultados: "+str(self.totalEncontrado))

    def setearFilas(self,filas):
        self.tableViewAux.limpiar_tabla()
        self.tableViewAux.agregar_filas(filas)
    
    def descargarResultados(self):
        self.tableViewAux.guardar_datos_visibles()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = VentanaPrincipal()  # Usa la clase VentanaPrincipal como la ventana principal
    #print(datetime.datetime.now().year)
    GUI.showMaximized()
    sys.exit(app.exec_())
    