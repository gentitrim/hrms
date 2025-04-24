// Funzione per creare la tabella iniziale
function createInitialTable() {
    const tableBody = document.querySelector('#menuTable tbody');
    tableBody.innerHTML = ''; // Pulisce la tabella

    for (const category in products) {
        // Aggiungi la riga della categoria
        const categoryRow = document.createElement('tr');
        categoryRow.classList.add('category-row');
        categoryRow.innerHTML = `
            <td>${category}</td>
            <td></td>
        `;
        tableBody.appendChild(categoryRow);

        // Aggiungi i prodotti della categoria
        products[category].forEach(product => {
            const productRow = document.createElement('tr');
            productRow.classList.add('product-row');
            productRow.style.display = 'none'; // Nascondi i prodotti inizialmente
            productRow.innerHTML = `
                <td></td>
                <td>${product.name}</td>
            `;
            tableBody.appendChild(productRow);


            productRow.addEventListener('click', () => {
                addSelectedProduct(product);
                updateTotal();
            });
        });


        categoryRow.addEventListener('click', () => {
            const productRows = Array.from(tableBody.querySelectorAll('.product-row'));
            productRows.forEach(row => {
                if (row.previousElementSibling === categoryRow) {
                    row.style.display = row.style.display === 'none' ? 'table-row' : 'none';
                }
            });
        });
    }
}


function addSelectedProduct(product) {
    const selectedTableBody = document.querySelector('#selectedProductsTable tbody');
    const existingRow = Array.from(selectedTableBody.children).find(row => row.querySelector('td').textContent === product.name);

    if (existingRow) {
        const quantityCell = existingRow.querySelector('td:nth-child(2)');
        const quantity = parseInt(quantityCell.textContent) + 1;
        quantityCell.textContent = quantity;
        const totalCell = existingRow.querySelector('td:nth-child(4)');
        totalCell.textContent = (quantity * product.price).toFixed(2) + ' €';
    } else {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${product.name}</td>
            <td>1</td>
            <td>${product.price.toFixed(2)} €</td>
            <td>${product.price.toFixed(2)} €</td>
            <td><button class="remove-btn">Rimuovi</button></td>
        `;
        selectedTableBody.appendChild(newRow);


        newRow.querySelector('.remove-btn').addEventListener('click', () => {
            selectedTableBody.removeChild(newRow);
            updateTotal();
        });
    }
}


function updateTotal() {
    let total = 0;
    const rows = document.querySelectorAll('#selectedProductsTable tbody tr');

    rows.forEach(row => {
        const totalCell = row.querySelector('td:nth-child(4)');
        total += parseFloat(totalCell.textContent);
    });

    document.getElementById('totalPrice').textContent = total.toFixed(2) + ' €';
}


createInitialTable();

// // Hamburger menu toggle
// const hamburger = document.querySelector('.hamburger');
// const navUl = document.querySelector('#nav ul');

// hamburger.addEventListener('click', () => {
//     navUl.classList.toggle('active');
// });


document.getElementById('clearSelection').addEventListener('click', () => {
    const selectedTableBody = document.querySelector('#selectedProductsTable tbody');
    selectedTableBody.innerHTML = '';
    updateTotal();
});


document.getElementById('printInvoice').addEventListener('click', () => {
    const printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write('<html><head><title>Fattura</title>');
    printWindow.document.write(`
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            h1 {
                text-align: center;
                color: #1E50A2;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
            }
            th {
                background-color: #1E50A2;
                color: white;
            }
            .total-price {
                font-weight: bold;
                text-align: right;
            }
        </style>
    `);
    printWindow.document.write('</head><body>');
    printWindow.document.write('<h1>Fattura</h1>');
    printWindow.document.write(document.getElementById('selectedProductsTable').outerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
});