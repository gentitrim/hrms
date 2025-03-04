$(document).ready(function(){
    $("#category_fetch").click(function(){
        let pk = $(this).data("foreign-key");
        $.ajax({
            url: `{% url 'get_products' ${pk} %}`,
            type: "GET",
            success: function(response) {
                $("#result").html(""); // Clear previous results
                response.forEach(function(item) {
                    $("#result").append(`<p>${product.name} - ${product.price}</p>`);
                });
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    });
});