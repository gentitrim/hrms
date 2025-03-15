document.body.addEventListener("click", (event) => {
    // ✅ Handle "Add to Order"
    if (event.target.classList.contains("add-to-order")) {
        const button = event.target;
        const productId = button.getAttribute("data-product-id");
        const product = button.getAttribute("data-product");
        const price = parseFloat(button.getAttribute("data-price"));
        const orderTableBody = document.querySelector("#selectedProductsTable tbody");
        const totalPriceElement = document.getElementById("totalPrice");

        console.log(`Adding product: ${product}, Price: ${price}`);

        // Ensure totalPrice is correctly retrieved
        let totalPrice = parseFloat(totalPriceElement.textContent) || 0;

        // Check if product already exists in the order
        let existingRow = [...orderTableBody.querySelectorAll("tr")].find(row => {
            return row.querySelector("td").textContent === product;
        });

        if (existingRow) {
            // Update quantity and total
            let quantityCell = existingRow.querySelector("td:nth-child(2)");
            let totalCell = existingRow.querySelector("td:nth-child(4)");
            let quantity = parseInt(quantityCell.textContent, 10) + 1;
            quantityCell.textContent = quantity;
            totalCell.textContent = (quantity * price).toFixed(2) + " €";
        } else {
            // Add new row for the product
            let newRow = document.createElement("tr");
            newRow.setAttribute("data-product-id", productId);
            newRow.innerHTML = `
                <td>${product}</td>
                <td>1</td>
                <td>${price.toFixed(2)} €</td>
                <td>${price.toFixed(2)} €</td>
                <td><button class="remove-item">Remove</button></td>
            `;
            orderTableBody.appendChild(newRow);
        }

        // Update total price
        totalPrice += price;
        totalPriceElement.textContent = totalPrice.toFixed(2) + " €";
    }

    // ✅ Handle "Remove Item"
    if (event.target.classList.contains("remove-item")) {
        const row = event.target.closest("tr");
        const totalCell = row.querySelector("td:nth-child(4)");
        let price = parseFloat(totalCell.textContent);
        const totalPriceElement = document.getElementById("totalPrice");

        console.log(`Removing item, Price: ${price}`);

        let totalPrice = parseFloat(totalPriceElement.textContent) || 0;
        totalPrice -= price;
        totalPriceElement.textContent = totalPrice.toFixed(2) + " €";
        row.remove();
    }

    // ✅ Handle "Clear Order"
    if (event.target.id === "clearSelection") {
        console.log("Clearing selection");
        document.querySelector("#selectedProductsTable tbody").innerHTML = "";
        document.getElementById("totalPrice").textContent = "0.00 €";
    }

    // ✅ Handle "Print Invoice"
    if (event.target.id === "printInvoice") {
        console.log("Printing invoice...");
        // alert("Invoice printed!"); // Replace with actual print functionality
    }
});

// ✅ Ensure JavaScript Runs After HTMX Updates
document.body.addEventListener("htmx:afterSettle", () => {
    console.log("HTMX content updated - JavaScript is still working!");
});


// Function to get the CSRF token
// Function to get the CSRF token
function getCsrfToken() {
    return document.querySelector("input[name='csrfmiddlewaretoken']").value;
}

// Function to get order items from the table
function getOrderItems() {
    const rows = document.querySelectorAll('#selectedProductsTable tbody tr');
    const items = [];

    rows.forEach((row) => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 4) {
            const productId = row.getAttribute('data-product-id'); // Get product ID
            items.push({
                product_id: parseInt(productId, 10), // Include product ID
                product_name: cells[0].innerText.trim(),
                quantity: parseInt(cells[1].innerText.trim(), 10),
                price: parseFloat(cells[2].innerText.replace(' €', '').trim()),
                total_price: parseFloat(cells[3].innerText.replace(' €', '').trim())
            });
        }
    });

    return items;
}

// Get references to the dialog and buttons
const dialog = document.getElementById('confirmationDialog');
const printInvoiceButton = document.getElementById('printInvoice');
const confirmOrderButton = document.getElementById('confirmOrder');
const cancelOrderButton = document.getElementById('cancelOrder');

// Open the dialog when the Print Invoice button is clicked
printInvoiceButton.addEventListener('click', function() {
    dialog.showModal(); // Open the dialog
});


// Handle confirmation
confirmOrderButton.addEventListener('click', function() {
    const csrfToken = getCsrfToken();
    const items = getOrderItems();

    console.log('CSRF Token:', csrfToken); // Debugging
    console.log('Order items:', items); // Debugging

    // Send the order data to the server
    fetch('/restaurant/confirm_order/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ items: items })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data); // Debugging

        // Display only the message from the response
        const responseDiv = document.getElementById('response');
        responseDiv.innerText = data.message; // Show the message
        document.querySelector("#selectedProductsTable tbody").innerHTML = "";
        document.getElementById("totalPrice").textContent = "0.00 €";
        // Hide the message after 3 seconds
        setTimeout(() => {
            responseDiv.innerText = ''; // Clear the message
        }, 3000); // 3 seconds
    })
    .catch(error => {
        console.error('Error:', error); // Debugging

        // Display the error message
        const responseDiv = document.getElementById('response');
        responseDiv.innerText = 'An error occurred. Please try again.';

        // Hide the error message after 3 seconds
        setTimeout(() => {
            responseDiv.innerText = ''; // Clear the message
        }, 3000); // 3 seconds
    });

    dialog.close(); // Close the dialog
});