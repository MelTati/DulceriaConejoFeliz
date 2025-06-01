import mysql.connector
from db.conexion import crear_conexion

class VentasModel:
    def obtener_usuarios(self):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.id_usuario, u.nombre_usuario, u.telefono, r.cargo
                FROM usuarios u
                JOIN roles r ON u.id_roles = r.id_roles
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    def obtener_clientes(self):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_cliente, nombre, telefono FROM cliente")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    def obtener_ventas(self):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT v.id_ventas, v.fecha_venta,
                       u.nombre_usuario, c.nombre AS nombre_cliente,
                       IFNULL(SUM(dv.subtotal), 0) AS total
                FROM ventas v
                JOIN usuarios u ON v.id_usuario = u.id_usuario
                JOIN cliente c ON v.id_cliente = c.id_cliente
                LEFT JOIN detalles_ventas dv ON v.id_ventas = dv.id_ventas
                GROUP BY v.id_ventas
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    def crear_venta(self, fecha, id_usuario, id_cliente):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO ventas (fecha_venta, id_usuario, id_cliente)
                VALUES (%s, %s, %s)
            """, (fecha, id_usuario, id_cliente))
            conexion.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conexion.close()

    def actualizar_venta(self, id_venta, fecha, id_usuario, id_cliente):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE ventas
                SET fecha_venta=%s, id_usuario=%s, id_cliente=%s
                WHERE id_ventas=%s
            """, (fecha, id_usuario, id_cliente, id_venta))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def eliminar_venta(self, id_venta):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM ventas WHERE id_ventas = %s", (id_venta,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    #Función interna para actualizar el total en la tabla ventas
    def _actualizar_total_en_ventas(self, id_venta, total):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE ventas SET total = %s WHERE id_ventas = %s
            """, (total, id_venta))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def obtener_total_venta(self, id_venta):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT IFNULL(SUM(dv.subtotal), 0) AS total
                FROM detalles_ventas dv
                WHERE dv.id_ventas = %s
            """, (id_venta,))
            total = cursor.fetchone()['total']
            # Actualiza el total en la tabla ventas
            self._actualizar_total_en_ventas(id_venta, total)
            return total
        finally:
            cursor.close()
            conexion.close()

    def obtener_venta_por_id(self, id_venta):
        try:
            # Primero actualiza el total antes de consultar la venta
            total = self.obtener_total_venta(id_venta)
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT v.id_ventas, v.fecha_venta,
                       u.nombre_usuario, c.nombre AS nombre_cliente,
                       v.total
                FROM ventas v
                JOIN usuarios u ON v.id_usuario = u.id_usuario
                JOIN cliente c ON v.id_cliente = c.id_cliente
                WHERE v.id_ventas = %s
            """, (id_venta,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexion.close()