$(document).ready(function(){
    $("#category_fetch").click(function(){
        let pk = $(this).data('pk');
        $.ajax({
            url: "{% url 'get_products' ${pk} %}",
            type: "GET",
            success: function(response) {
                console.log(response);
                // $("#result").html(""); // Clear previous results
                // response.forEach(function(item) {
                //     console.log(item);
                    // $("#result").append(`<p>${  item.name } - ${ item.price }</p>`);
                // };
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    });
});