$(".nav .nav-link").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).addClass("active");
});
function loading(){
    $("#loading").show();
    $("#content").hide();
}
