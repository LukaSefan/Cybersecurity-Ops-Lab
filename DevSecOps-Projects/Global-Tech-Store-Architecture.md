# Arquitectura de Software: E-commerce "Global Tech Store"

## 📋 Resumen del Proyecto
Desarrollo e implementación de una plataforma web "Full-Stack" para comercio electrónico de productos tecnológicos. El sistema utiliza una arquitectura desacoplada con una API RESTful en **ASP.NET Core 8**, persistencia en **MySQL** y un frontend dinámico en **JavaScript (ES6)**.

## ⚙️ Stack Tecnológico
| Capa | Tecnología | Rol |
| :--- | :--- | :--- |
| **Backend** | ASP.NET Core 8 (C#) | API REST, Lógica de Negocio |
| **Base de Datos** | MySQL + Entity Framework Core | Persistencia Relacional |
| **Frontend** | HTML5, CSS3, JavaScript | Interfaz de Usuario (SPA) |
| **ORM** | Pomelo.EntityFrameworkCore | Mapeo Objeto-Relacional |

---

## 🏗️ Arquitectura del Sistema (Patrón MVC)
Se implementó una arquitectura basada en el patrón Modelo-Vista-Controlador para garantizar la escalabilidad.

### La Analogía del Restaurante (Explicación Conceptual)
Para documentar el flujo de datos, utilizamos la analogía de un restaurante profesional:

1.  **La Vista (El Menú - Frontend):**
    * Los archivos `Eccomers.html` y `pago.html` actúan como el menú. Muestran los productos disponibles y capturan las órdenes del cliente (Inputs), pero no cocinan nada.

2.  **El Controlador (El Mesero - API Controllers):**
    * `ProductosController` y `OrdenesController` reciben la comanda (JSON). Su trabajo es validar que el pedido sea correcto (Stock suficiente, datos válidos) antes de pasarlo a la cocina.

3.  **El Modelo (La Cocina - Entity Framework):**
    * Las clases `Producto`, `Orden` y `Usuario` definen los ingredientes y recetas. Es aquí donde la lógica de negocio interactúa con la bodega (Base de Datos MySQL) para preparar la respuesta final.

---

## 💻 Implementación Técnica (Backend)

### Modelo de Datos (Entity Framework)
Definición de entidades con relaciones relacionales para mantener la integridad de las transacciones.

```csharp
// --- Models/Producto.cs ---
public class Producto
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public decimal Precio { get; set; }
    public int Stock { get; set; }
    // Relación con OrdenesDetalle para historial de ventas
    public ICollection<OrdenDetalle> OrdenesDetalle { get; set; }
}

// --- Models/Orden.cs ---
public class Orden
{
    public int Id { get; set; }
    public int UsuarioId { get; set; }
    public DateTime Fecha { get; set; }
    public decimal Total { get; set; }
    public ICollection<OrdenDetalle> OrdenesDetalle { get; set; }
}
Lógica de Controladores (API)
Endpoint transaccional para la creación de órdenes, manejando validación de stock y cálculo de totales en el servidor (Seguridad).

C#

// --- Controllers/OrdenesController.cs ---
[HttpPost]
public async Task<IActionResult> CrearOrden([FromBody] CrearOrdenDto dto)
{
    // 1. Validaciones y creación de Usuario (Lógica simplificada)
    var orden = new Orden { /* ... */ };

    // 2. Procesamiento de Stock (Atomicidad)
    foreach (var item in dto.Productos)
    {
        var producto = await _context.Productos.FindAsync(item.ProductoId);
        if (producto.Stock < item.Cantidad)
            return BadRequest($"Stock insuficiente: {item.ProductoId}");
        
        producto.Stock -= item.Cantidad; // Decremento de inventario
        orden.Total += producto.Precio * item.Cantidad; // Cálculo seguro en backend
    }
    
    // 3. Persistencia (Commit)
    _context.Ordenes.Add(orden);
    await _context.SaveChangesAsync();
    return Ok(new { message = "Orden creada", ordenId = orden.Id });
}
🎨 Implementación Técnica (Frontend)
Gestión del Estado (Carrito de Compras)
Lógica en JavaScript para manejar el estado local del carrito y la sincronización con el localStorage.

JavaScript

// Lógica de Agregar al Carrito con validación de Stock local
function agregarAlCarrito(productoId) {
    const producto = productosDisponibles.find(p => p.id === productoId);
    
    // Validación preventiva en cliente
    if (!producto || producto.stock <= (carrito.find(item => item.id === productoId)?.cantidad || 0)) {
        alert('Stock insuficiente.');
        return;
    }

    const itemExistente = carrito.find(item => item.id === productoId);
    if (itemExistente) {
        itemExistente.cantidad++;
    } else {
        carrito.push({ ...producto, cantidad: 1 });
    }
    actualizarCarrito(); // Renderizado reactivo
}
🔒 Consideraciones de Seguridad (DevSecOps)
Cálculo en Servidor: El total a pagar se calcula estrictamente en el Backend (OrdenesController), ignorando cualquier precio enviado desde el Frontend para evitar manipulación de precios.

Validación de Stock: Doble verificación de inventario (Frontend preventivo + Backend autoritativo) para evitar condiciones de carrera (Race Conditions).

DTOs (Data Transfer Objects): Uso de CrearOrdenDto para exponer solo los datos necesarios y proteger la estructura interna de la base de datos.
