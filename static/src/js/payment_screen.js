/** 
 * MÓDULO: pos_kitchen_order
 * ARCHIVO: payment_screen.js
 * FUNCIÓN: Interceptar validación de pago e imprimir comanda automáticamente
 */

odoo.define('pos_kitchen_order.PaymentScreen', function (require) {
    'use strict';
    
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require('point_of_sale.Gui');
    
    const KitchenOrderPaymentScreen = PaymentScreen => class extends PaymentScreen {
        
        async validateOrder(isForceValidate) {
            const order = this.env.pos.get_order();
            
            // Verificar si hay productos para cocina
            const kitchenProducts = this._getKitchenProducts(order);
            
            if (kitchenProducts.length > 0 && this.env.pos.config.auto_print_kitchen) {
                try {
                    // Imprimir comanda de cocina PRIMERO
                    await this._printKitchenOrder(order, kitchenProducts);
                    
                    // Esperar un momento para que se procese
                    await new Promise(resolve => setTimeout(resolve, 500));
                    
                } catch (error) {
                    console.error('Error al imprimir comanda:', error);
                    await Gui.showPopup('ErrorPopup', {
                        title: 'Error de Impresión',
                        body: 'No se pudo imprimir la comanda de cocina. La venta continuará.',
                    });
                }
            }
            
            // Continuar con el proceso normal (imprime recibo)
            await super.validateOrder(isForceValidate);
        }
        
        _getKitchenProducts(order) {
            // Filtrar productos que van a cocina
            return order.get_orderlines().filter(line => {
                const product = line.get_product();
                // Verificar si el producto tiene marcado "send_to_kitchen"
                // O si pertenece a categorías específicas
                const kitchenCategories = ['Combos', 'Comidas', 'Bebidas', 'Postres'];
                
                return product.send_to_kitchen || 
                       (product.pos_categ_id && 
                        kitchenCategories.some(cat => 
                            product.pos_categ_id.name.includes(cat)));
            });
        }
        
        async _printKitchenOrder(order, products) {
            const receiptData = this._prepareKitchenReceiptData(order, products);
            const receiptHtml = this._renderKitchenReceipt(receiptData);
            
            // Crear iframe oculto para impresión
            const printFrame = document.createElement('iframe');
            printFrame.style.display = 'none';
            document.body.appendChild(printFrame);
            
            // Escribir contenido
            printFrame.contentDocument.open();
            printFrame.contentDocument.write(receiptHtml);
            printFrame.contentDocument.close();
            
            // Imprimir
            printFrame.contentWindow.focus();
            printFrame.contentWindow.print();
            
            // Limpiar
            setTimeout(() => {
                document.body.removeChild(printFrame);
            }, 1000);
        }
        
        _prepareKitchenReceiptData(order, products) {
            return {
                orderName: order.name || order.sequence_number || 'Nueva',
                date: new Date(),
                table: order.table ? order.table.name : 'Para Llevar',
                customer: order.get_partner() ? order.get_partner().name : 'Cliente General',
                cashier: this.env.pos.user.name,
                lines: products.map(line => ({
                    qty: Math.round(line.get_quantity()),
                    product: line.get_product().display_name,
                    note: line.get_customer_note() || ''
                }))
            };
        }
        
        _renderKitchenReceipt(data) {
            const dateStr = data.date.toLocaleString('es-GT', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            let itemsHtml = '';
            data.lines.forEach(line => {
                itemsHtml += `
                    <div class="kitchen-item">
                        <span class="kitchen-qty">${line.qty}</span>
                        <span class="kitchen-product">${line.product}</span>
                        ${line.note ? `<div class="kitchen-note">→ ${line.note}</div>` : ''}
                    </div>`;
            });
            
            return `
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Comanda ${data.orderName}</title>
                    <style>
                        @page { size: 80mm auto; margin: 0; }
                        @media print { 
                            body { margin: 0; }
                            .no-print { display: none; }
                        }
                        body {
                            width: 80mm;
                            margin: 0;
                            padding: 5mm;
                            font-family: 'Courier New', monospace;
                            font-size: 12pt;
                        }
                        .kitchen-header {
                            text-align: center;
                            font-weight: bold;
                            font-size: 16pt;
                            border-bottom: 3px double black;
                            padding-bottom: 3mm;
                            margin-bottom: 3mm;
                        }
                        .kitchen-info {
                            text-align: center;
                            margin-bottom: 3mm;
                        }
                        .kitchen-items-title {
                            text-align: center;
                            font-weight: bold;
                            border-top: 2px solid black;
                            border-bottom: 2px solid black;
                            padding: 2mm 0;
                            margin: 3mm 0;
                        }
                        .kitchen-item {
                            border-bottom: 1px dashed #999;
                            padding: 3mm 0;
                        }
                        .kitchen-qty {
                            display: inline-block;
                            width: 15mm;
                            text-align: center;
                            font-size: 18pt;
                            font-weight: bold;
                        }
                        .kitchen-product {
                            font-size: 14pt;
                            font-weight: bold;
                        }
                        .kitchen-note {
                            margin-left: 20mm;
                            font-style: italic;
                            font-size: 11pt;
                            color: #333;
                        }
                        .kitchen-footer {
                            text-align: center;
                            margin-top: 5mm;
                            padding-top: 3mm;
                            border-top: 3px double black;
                            font-weight: bold;
                            font-size: 14pt;
                        }
                    </style>
                </head>
                <body>
                    <div class="kitchen-header">
                        *** COMANDA COCINA ***<br>
                        ORDEN #${data.orderName}
                    </div>
                    
                    <div class="kitchen-info">
                        <strong>${dateStr}</strong><br>
                        Mesa: <strong>${data.table}</strong><br>
                        Cliente: ${data.customer}<br>
                        Cajero: ${data.cashier}
                    </div>
                    
                    <div class="kitchen-items-title">
                        === PREPARAR LOS SIGUIENTES ITEMS ===
                    </div>
                    
                    <div class="kitchen-items">
                        ${itemsHtml}
                    </div>
                    
                    <div class="kitchen-footer">
                        *** PREPARAR INMEDIATAMENTE ***<br>
                        ¡ORDEN NUEVA!
                    </div>
                    
                    <div style="height: 30mm;"></div>
                </body>
                </html>`;
        }
    };
    
    Registries.Component.extend(PaymentScreen, KitchenOrderPaymentScreen);
    
    return KitchenOrderPaymentScreen;
});
