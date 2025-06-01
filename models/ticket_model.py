from db.conexion import crear_conexion

class TicketModel:
    def __init__(self):
        self.conexion = crear_conexion()
        self.cursor = self.conexion.cursor(dictionary=True)

    def obtener_todos(self):
        try:
            self.cursor.execute("""
                SELECT
                    t.id_ticket,
                    m.tipo AS modo_pago,
                    v.id_ventas,
                    v.fecha_venta,
                    u.nombre_usuario AS nombre_usuario,
                    c.nombre AS nombre_cliente,
                    t.cantidad_pagada,
                    t.cambio
                FROM ticket t
                JOIN modo_pago m ON t.id_modo_pago = m.id_modo_pago
                JOIN ventas v ON t.id_ventas = v.id_ventas
                JOIN usuarios u ON v.id_usuario = u.id_usuario
                JOIN cliente c ON v.id_cliente = c.id_cliente
            """)
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def obtener_modos_pago(self):
        try:
            self.cursor.execute("SELECT id_modo_pago, tipo FROM modo_pago")
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def obtener_ventas(self):
        try:
            self.cursor.execute("""
                SELECT v.id_ventas, v.fecha_venta, u.nombre_usuario, c.nombre AS nombre_cliente
                FROM ventas v
                JOIN usuarios u ON v.id_usuario = u.id_usuario
                JOIN cliente c ON v.id_cliente = c.id_cliente
            """)
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def crear_ticket(self, id_ticket, id_modo_pago, id_ventas, cantidad_pagada=None):
        try:
            self.cursor.execute("""
                INSERT INTO ticket (id_ticket, id_modo_pago, id_ventas, cantidad_pagada)
                VALUES (%s, %s, %s, %s)
            """, (id_ticket, id_modo_pago, id_ventas, cantidad_pagada))
            self.conexion.commit()
            # Actualiza el cambio automáticamente después de crear el ticket
            self.actualizar_cambio(id_ticket)
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e

    def actualizar_ticket(self, id_ticket, id_modo_pago, id_ventas, cantidad_pagada=None):
        try:
            self.cursor.execute("""
                UPDATE ticket
                SET id_modo_pago=%s, id_ventas=%s, cantidad_pagada=%s
                WHERE id_ticket=%s
            """, (id_modo_pago, id_ventas, cantidad_pagada, id_ticket))
            self.conexion.commit()
            # Actualiza el cambio automáticamente después de actualizar el ticket
            self.actualizar_cambio(id_ticket)
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e

    def actualizar_cambio(self, id_ticket):
        """
        Actualiza el campo 'cambio' en el ticket como cantidad_pagada - (total * 1.16) de la venta relacionada.
        """
        try:
            self.cursor.execute("""
                SELECT t.cantidad_pagada, v.total
                FROM ticket t
                JOIN ventas v ON t.id_ventas = v.id_ventas
                WHERE t.id_ticket = %s
            """, (id_ticket,))
            datos = self.cursor.fetchone()
            if datos and datos['cantidad_pagada'] is not None and datos['total'] is not None:
                total_con_iva = float(datos['total']) * 1.16
                cambio = float(datos['cantidad_pagada']) - total_con_iva
            else:
                cambio = None
            self.cursor.execute("""
                UPDATE ticket SET cambio = %s WHERE id_ticket = %s
            """, (cambio, id_ticket))
            self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            raise e

    def eliminar_ticket(self, id_ticket):
        try:
            self.cursor.execute("DELETE FROM ticket WHERE id_ticket=%s", (id_ticket,))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_detalles_impresion(self, id_ticket):
        try:
            self.cursor.execute("""
                SELECT
                    t.id_ticket,
                    m.tipo AS modo_pago,
                    v.id_ventas,
                    v.fecha_venta,
                    u.nombre_usuario AS nombre_usuario,
                    u.telefono AS telefono_usuario,
                    c.nombre AS nombre_cliente,
                    c.telefono AS telefono_cliente,
                    a.codigo_articulo,
                    a.nombre_articulo,
                    dv.cantidad,
                    dv.subtotal,
                    t.cantidad_pagada,
                    t.cambio
                FROM ticket t
                JOIN modo_pago m ON t.id_modo_pago = m.id_modo_pago
                JOIN ventas v ON t.id_ventas = v.id_ventas
                JOIN usuarios u ON v.id_usuario = u.id_usuario
                JOIN cliente c ON v.id_cliente = c.id_cliente
                JOIN detalles_ventas dv ON v.id_ventas = dv.id_ventas
                JOIN articulos a ON dv.codigo_articulo = a.codigo_articulo
                WHERE t.id_ticket = %s
            """, (id_ticket,))
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def __del__(self):
        if self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()