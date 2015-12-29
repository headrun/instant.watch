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
  function show_movie_details(){
      $("#movie-detail").removeClass("hide");
  }
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

  $(".tv-cover").css('background-image','url("static/web/images/the-revenant-posters.jpg")');

 // $(".tv-poster-background").css('background-image','url("static/web/images/the-revenant-posters.jpg")');
  $(".list_region_movies .list .items .item").on("click",function(){
    var id = parseInt($(this).attr("data-id"));
    $(".list_region_movies .list .spinner").removeClass("hide");
    console.log("working1");
    console.log(id);
    $.ajax({
      type: "post",
      url: "movies/",
      data: { "send_data":id,
              csrfmiddlewaretoken: '{{ csrf_token }}'
            },
      success: function(Data){
               console.log("success");
               $(".movie-detail .content-box .meta-container .title").text(Data["name"]);
               $(".movie-detail .content-box .meta-container .metadatas .metaitem").eq(0).text(Data["year_of_release"]);
               $(".movie-detail .content-box .meta-container .metadatas .metaitem").eq(1).text(Data["duration"]+" min");
               $(".movie-detail .content-box .meta-container .metadatas .metaitem").eq(2).text(Data["genre"]);
               $(".movie-detail .content-box .meta-container .overview").text(Data["synopsys"]);
               $(".list_region_movies .list .spinner").addClass("hide");
               show_movie_details();
            }
    });
  });


  function getCookie(name){
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
          }
        }
      }
    return cookieValue;
  }

  $.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
      } 
  }); 
 });
