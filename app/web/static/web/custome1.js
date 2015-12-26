$(function(){
  "use strict";

  function myFunction(){
    var $get_item = $(".list-region.show > .list > .items > .item").eq(0);
    var $set_item = $(".list-region > .list > .items > .item");
    var margin = 10
    $set_item.css({"margin-left":margin,"margin-right":margin});
    var item_wid = $get_item.width();
    item_wid = item_wid +(2*(parseInt($get_item.css("margin-left"))));
  //  console.log("item:"+item_wid);
    var row_wid = $(".display_items > .show > .list > .items > .item").parent().width();
    var items_num=parseInt(row_wid/item_wid);
    var result_wid = (row_wid % item_wid);
    var padd = result_wid/items_num;
    var padding =Math.floor(padd/2);
    var add_margin = parseInt($get_item.css("margin-left"));
    $set_item.css({"margin-left":add_margin+padding,"margin-right":add_margin+padding});
//    console.log("item wid:"+item_wid+"row width:"+row_wid+"margin left:"+add_margin+"add:"+padding);
  }

  myFunction();

  $(window).resize(function(){ myFunction();});

  $(".showShows").on("click",function(){
    $(".showMovies").removeClass("active") ;
    $(".list_region_movies").addClass("hide").removeClass("show");
    $(".list_region_series").addClass("show").removeClass("hide");
    $(".showShows").addClass("active");
  });

  $(".showMovies").on("click",function(){
    $(".showShows").removeClass("active");
    $(".list_region_series").addClass("hide").removeClass("show");
    $(".list_region_movies").addClass("show").removeClass("hide");
    $(".showMovies").addClass("active");
   });
  $(".list-region.list_region_movies > .list > .items > .item > .cover").on("click",function(){
    $("#movie-detail").removeClass("hide");
  });
  $(".movie-detail > .close-icon").on("click",function(){
    $("#movie-detail").addClass("hide");
  });
  $(".list-region.list_region_series > .list > .items > .item").on("click",function(){
    $(".shows-container-contain").removeClass("hide");
  });
  $(".shows-container-contain > .close-icon").on("click",function(){
    $(".shows-container-contain").addClass("hide");
  });
  $(".nav.nav-hor.left").on("click",function(){
    $("#movie-detail").addClass("hide");
    $(".shows-container-contain").addClass("hide");
  });
  $(".list_region_movies .list .items .item").on("click",function(){
   var id = $(this).attr("data-id");
   console.log(id);
  });

  $(".tv-cover").css('background-image','url("static/web/images/the-revenant-posters.jpg")');

 // $(".tv-poster-background").css('background-image','url("static/web/images/the-revenant-posters.jpg")');
  $(".list_region_movies .list .items").each(".item",function(){
    $(this).on("click",function(){
      var $id = $(this).attr("data-id");
      console.log("working1");
      console.log($id);
      $.ajax({
        type: "get",
        url: "web/movies/"+$id+"/",
        data: $id,
        success: function(responseData){
                 console.log("success");
              }
      });
    });
  });
 });
