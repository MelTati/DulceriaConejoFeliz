from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QDateEdit
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QIcon

from controllers.ventas_controllers import VentasController
from views.cliente_view import ClienteView
from views.detalles_ventas_views import VentanaDetallesVentas

class VentanaVentas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Ventas")
        self.controlador = VentasController()
        self.init_ui()
        self.cargar_datos()

    def init_ui(self):
        layout = QVBoxLayout()

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID Venta", "Fecha", "Usuario", "Cliente", "Total"])
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        layout.addWidget(self.tabla)

        # Controles de formulario
        form_layout = QHBoxLayout()
        self.input_fecha = QDateEdit()
        self.input_fecha.setDisplayFormat("yyyy-MM-dd")
        self.input_fecha.setDate(QDate.currentDate())
        self.combo_usuarios = QComboBox()
        self.combo_clientes = QComboBox()
        form_layout.addWidget(self.input_fecha)
        form_layout.addWidget(self.combo_usuarios)
        form_layout.addWidget(self.combo_clientes)
        layout.addLayout(form_layout)

        # Botones
        botones_layout = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar", icon=QIcon("icons/add.png"))
        self.btn_actualizar = QPushButton("Actualizar", icon=QIcon("icons/update.png"))
        self.btn_eliminar = QPushButton("Eliminar", icon=QIcon("icons/delete.png"))
        self.btn_clientes = QPushButton("Clientes", icon=QIcon("icons/clients.png"))
        self.btn_detalles = QPushButton("Detalles", icon=QIcon("icons/details.png"))

        self.btn_agregar.clicked.connect(self.agregar_venta)
        self.btn_actualizar.clicked.connect(self.actualizar_venta)
        self.btn_eliminar.clicked.connect(self.eliminar_venta)
        self.btn_clientes.clicked.connect(self.abrir_clientes)
        self.btn_detalles.clicked.connect(self.abrir_detalles)

        botones_layout.addWidget(self.btn_agregar)
        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_clientes)
        botones_layout.addWidget(self.btn_detalles)
        layout.addLayout(botones_layout)

        self.setLayout(layout)

    def cargar_datos(self):
        # Cargar comboboxes
        self.combo_usuarios.clear()
        for usuario in self.controlador.obtener_usuarios():
            self.combo_usuarios.addItem(
                f"{usuario['nombre_usuario']} ({usuario['telefono']})",
                usuario['id_usuario']
            )

        self.combo_clientes.clear()
        for cliente in self.controlador.obtener_clientes():
            self.combo_clientes.addItem(
                f"{cliente['nombre']} ({cliente['telefono']})",
                cliente['id_cliente']
            )

        # Cargar tabla
        self.tabla.setRowCount(0)
        for venta in self.controlador.obtener_ventas():
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(venta['id_ventas'])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(venta['fecha_venta'])))
            self.tabla.setItem(fila, 2, QTableWidgetItem(venta['nombre_usuario']))
            self.tabla.setItem(fila, 3, QTableWidgetItem(venta['nombre_cliente']))
            self.tabla.setItem(fila, 4, QTableWidgetItem(f"${venta['total']:.2f}"))

    def seleccionar_fila(self, fila, _):
            self.input_fecha.setDate(QDate.fromString(self.tabla.item(fila, 1).text(), "yyyy-MM-dd"))
            usuario_texto = self.tabla.item(fila, 2).text().split(" (")[0]
            cliente_texto = self.tabla.item(fila, 3).text().split(" (")[0]

            index_usuario = self.combo_usuarios.findText(usuario_texto, Qt.MatchStartsWith)
            index_cliente = self.combo_clientes.findText(cliente_texto, Qt.MatchStartsWith)

            if index_usuario != -1:
                self.combo_usuarios.setCurrentIndex(index_usuario)
            if index_cliente != -1:
                self.combo_clientes.setCurrentIndex(index_cliente)

    def agregar_venta(self):
        try:
            self.controlador.agregar_venta(
                self.input_fecha.date().toString("yyyy-MM-dd"),
                self.combo_usuarios.currentData(),
                self.combo_clientes.currentData()
            )
            QMessageBox.information(self, "Éxito", "Venta agregada correctamente")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def actualizar_venta(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            try:
                self.controlador.actualizar_venta(
                    int(self.tabla.item(fila, 0).text()),
                    self.input_fecha.date().toString("yyyy-MM-dd"),
                    self.combo_usuarios.currentData(),
                    self.combo_clientes.currentData()
                )
                QMessageBox.information(self, "Éxito", "Venta actualizada")
                self.cargar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def eliminar_venta(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            try:
                self.controlador.eliminar_venta(int(self.tabla.item(fila, 0).text()))
                QMessageBox.information(self, "Éxito", "Venta eliminada")
                self.cargar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def abrir_clientes(self):
        self.ventana_clientes = ClienteView()
        self.ventana_clientes.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.ventana_clientes.destroyed.connect(self.cargar_datos)
        self.ventana_clientes.show()

    def abrir_detalles(self):
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione una venta para ver sus detalles.")
            return

        venta_id = int(self.tabla.item(fila_seleccionada, 0).text())

        if hasattr(self, 'detalles_ventas'):
            self.detalles_ventas.close()

        self.detalles_ventas = VentanaDetallesVentas(venta_id)
        self.detalles_ventas.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.detalles_ventas.detalle_modificado.connect(
            lambda: self.actualizar_fila_venta(venta_id))
        self.detalles_ventas.show()

    def actualizar_fila_venta(self, venta_id):
        for fila in range(self.tabla.rowCount()):
            if int(self.tabla.item(fila, 0).text()) == venta_id:
                venta = self.controlador.obtener_venta_por_id(venta_id) 
                if venta:
                    self.tabla.setItem(fila, 1, QTableWidgetItem(str(venta['fecha_venta'])))
                    self.tabla.setItem(fila, 2, QTableWidgetItem(venta['nombre_usuario']))
                    self.tabla.setItem(fila, 3, QTableWidgetItem(venta['nombre_cliente']))
                    self.tabla.setItem(fila, 4, QTableWidgetItem(f"${venta['total']:.2f}"))
                break
