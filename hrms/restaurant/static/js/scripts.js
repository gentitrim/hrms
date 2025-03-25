document.body.addEventListener("click", (event) => {
    // ✅ Handle "Add to Order"
    if (event.target.classList.contains("add-to-order")) {
        const button = event.target;
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
        alert("Invoice printed!"); // Replace with actual print functionality
    }
});

// ✅ Ensure JavaScript Runs After HTMX Updates
document.body.addEventListener("htmx:afterSettle", () => {
    console.log("HTMX content updated - JavaScript is still working!");
});
