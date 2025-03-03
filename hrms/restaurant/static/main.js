$(document).ready(function(){
    $("#category_fetch").click(function(){
        let foreignKeyValue = $(this).data("foreign-key");
        $.ajax({
            url: 'get_roducts/$<pk>/',
            type: "GET",
            success: function(response) {
                $("#result").html(""); // Clear previous results
                response.forEach(function(item) {
                    $("#result").append('<p>${JSON.stringify(item)}</p>');
                });
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    });
});