$(function(){
  "use strict";

  function myFunction(){
    var $get_item = $(".list-region.show > .list > .items > .item").eq(0);
    var $set_item = $(".list-region > .list > .items > .item");
    var margin = 10
    $set_item.css({"margin-left":margin,"margin-right":margin});
    var item_wid = $get_item.width();
    item_wid = item_wid +(2*(parseInt($get_item.css("margin-left"))));
    console.log("item:"+item_wid);
    var row_wid = $(".display_items > .show > .list > .items > .item").parent().width();
    var items_num=parseInt(row_wid/item_wid);
    var result_wid = (row_wid % item_wid);
    var padd = result_wid/items_num;
    var padding =Math.floor(padd/2);
    var add_margin = parseInt($get_item.css("margin-left"));
    $set_item.css({"margin-left":add_margin+padding,"margin-right":add_margin+padding});
    console.log("item wid:"+item_wid+"row width:"+row_wid+"margin left:"+add_margin+"add:"+padding);
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
 });
