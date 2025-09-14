/**
 * BOTÓN DE REIMPRESIÓN DE COMANDA
 */

odoo.define('pos_kitchen_order.ReprintKitchenButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');

    class ReprintKitchenButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
        
        async onClick() {
            const order = this.env.pos.get_order();
            
            if (!order || order.get_orderlines().length === 0) {
                await this.showPopup('ErrorPopup', {
                    title: 'Error',
                    body: 'No hay productos en la orden actual',
                });
                return;
            }
            
            // Obtener productos de cocina
            const kitchenProducts = order.get_orderlines().filter(line => {
                const product = line.get_product();
                const kitchenCategories = ['Combos', 'Comidas', 'Bebidas', 'Postres'];
                return product.send_to_kitchen || 
                       (product.pos_categ_id && 
                        kitchenCategories.some(cat => 
                            product.pos_categ_id.name.includes(cat)));
            });
            
            if (kitchenProducts.length === 0) {
                await this.showPopup('ErrorPopup', {
                    title: 'Sin productos de cocina',
                    body: 'No hay productos que enviar a cocina en esta orden',
                });
                return;
            }
            
            // Confirmar reimpresión
            const { confirmed } = await this.showPopup('ConfirmPopup', {
                title: 'Reimprimir Comanda',
                body: `¿Desea reimprimir la comanda de cocina con ${kitchenProducts.length} productos?`,
            });
            
            if (confirmed) {
                await this.printKitchenOrder(order, kitchenProducts);
                
                await this.showPopup('SuccessPopup', {
                    title: 'Comanda Enviada',
                    body: 'La comanda ha sido enviada a la impresora de cocina',
                });
            }
        }
        
        async printKitchenOrder(order, products) {
            // Usar el mismo método de impresión del PaymentScreen
            const PaymentScreen = this.env.pos.payment_screen;
            if (PaymentScreen && PaymentScreen._printKitchenOrder) {
                await PaymentScreen._printKitchenOrder(order, products);
            } else {
                // Método alternativo directo
                const receiptHtml = this.generateKitchenReceipt(order, products);
                const printWindow = window.open('', '', 'width=300,height=600');
                printWindow.document.write(receiptHtml);
                printWindow.document.close();
                printWindow.print();
                setTimeout(() => printWindow.close(), 1000);
            }
        }
        
        generateKitchenReceipt(order, products) {
            // Generar HTML de la comanda
            const dateStr = new Date().toLocaleString('es-GT');
            let itemsHtml = '';
            
            products.forEach(line => {
                const qty = Math.round(line.get_quantity());
                const name = line.get_product().display_name;
                const note = line.get_customer_note();
                
                itemsHtml += `
                    <div style="margin: 5px 0; font-size: 14pt;">
                        <strong>${qty} x ${name}</strong>
                        ${note ? `<br>→ ${note}` : ''}
                    </div>`;
            });
            
            return `
                <html>
                <head>
                    <style>
                        body { 
                            width: 80mm; 
                            font-family: monospace; 
                            padding: 5mm;
                        }
                        .header { 
                            text-align: center; 
                            font-weight: bold; 
                            font-size: 16pt;
                            border-bottom: 2px solid black;
                            margin-bottom: 10px;
                        }
                    </style>
                </head>
                <body>
                    <div class="header">
                        *** COMANDA COCINA ***<br>
                        REIMPRESIÓN<br>
                        ${order.name || 'Nueva Orden'}
                    </div>
                    <div style="text-align: center;">
                        ${dateStr}<br>
                        ${order.table ? 'Mesa: ' + order.table.name : 'Para Llevar'}
                    </div>
                    <hr>
                    ${itemsHtml}
                    <hr>
                    <div style="text-align: center; font-weight: bold;">
                        *** PREPARAR AHORA ***
                    </div>
                </body>
                </html>`;
        }
    }
    
    ReprintKitchenButton.template = 'ReprintKitchenButton';
    ReprintKitchenButton.defaultProps = {};
    
    ProductScreen.addControlButton({
        component: ReprintKitchenButton,
        condition: function() {
            return this.env.pos.config.enable_kitchen_reprint;
        },
    });
    
    Registries.Component.add(ReprintKitchenButton);
    
    return ReprintKitchenButton;
});
