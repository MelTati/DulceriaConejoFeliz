from PyQt6.QtCore import QObject
from models.ventas_models import VentasModel

class VentasController(QObject):

    def __init__(self):
        super().__init__()
        self.modelo = VentasModel()

    def obtener_usuarios(self):
        return self.modelo.obtener_usuarios()

    def obtener_clientes(self):
        return self.modelo.obtener_clientes()

    def obtener_ventas(self):
        return self.modelo.obtener_ventas()

    def agregar_venta(self, fecha, usuario_id, cliente_id):
        self.modelo.crear_venta(fecha, usuario_id, cliente_id)

    def actualizar_venta(self, venta_id, fecha, usuario_id, cliente_id):
        self.modelo.actualizar_venta(venta_id, fecha, usuario_id, cliente_id)
    
    def eliminar_venta(self, venta_id):
        self.modelo.eliminar_venta(venta_id)
       
    def obtener_total_venta(self, venta_id):
        return self.modelo.obtener_total_venta(venta_id)

    def obtener_venta_por_id(self, venta_id):
        return self.modelo.obtener_venta_por_id(venta_id)