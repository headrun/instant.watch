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

  show_movies();

  $(".showShows").on("click",function(){
    $(".showMovies").removeClass("active") ;
    $(".list_region_movies").addClass("hide").removeClass("show");
    show_series();
    $(".showShows").addClass("active");
  });

  $(".showMovies").on("click",function(){
    $(".showShows").removeClass("active");
    $(".list_region_series").addClass("hide").removeClass("show");
    show_movies();
    $(".showMovies").addClass("active");
   });

  function show_movie_details(){
      $("#movie-detail").removeClass("hide");
  }

  $(".movie-detail > .close-icon").on("click",function(){
    $("#movie-detail").addClass("hide");
  });

  function show_series_details(){
    $(".shows-container-contain").removeClass("hide");
  }
  $(".shows-container-contain > .close-icon").on("click",function(){
    $(".shows-container-contain").addClass("hide");
  });

  $(".nav.nav-hor.left").on("click",function(){
    $("#movie-detail").addClass("hide");
    $(".shows-container-contain").addClass("hide");
  });

  $(".tv-cover").css('background-image','url("static/web/images/the-revenant-posters.jpg")');


 /* movie  details */

  $(".list_region_movies .list .items .item").on("click",function(){
    var id = parseInt($(this).attr("data-id"));
    $(".list_region_movies .list .spinner").removeClass("hide");
    console.log("working1");
    console.log(id);
    var show = "#details"+"_"+id;
    if ( $(show).length() > 0){
        $(show).removeClass("hide");
      }
    else{
      $.ajax({
        type: "post",
        url: "movies/",
        data: { "send_data":id,
              },
        success: function(Data){
                 console.log("success");
                 var templateRawText = $(".movie-detail").html();
                 var compiledTemplate = _.template(templateRawText);
                 var templateResult = compiledTemplate({name:"titanic","id":123,"year":1994});
                 $(".movie-detail").html(templateResult);
                 $(".movie-detail").attr("id",show);
                 $(".list_region_movies .list .spinner").addClass("hide");
                 show_movie_details();
              }
      });
    }
  });

  /*series details */

  $(".list_region_series .list .items .item").on("click",function(){
     var id = parseInt($(this).attr("data-id"));
     $(".list_region_series .list .spinner").removeClass("hide");
     console.log("working1");
     console.log(id);
     var show = "#details"+"_"+id;
     if ( $(show).length() > 0){
         $(show).removeClass("hide");
       }
     else{
       $.ajax({
         type: "post",
         url: "series/",
         data: { "send_data":id,
               },
         success: function(Data){
                  console.log("success");
                  var templateRawText = $(".series-detail").html();
                  var compiledTemplate = _.template(templateRawText);
                  var templateResult = compiledTemplate({name:"titanic","id":123,"year":1994});
                  $(".series-detail").html(templateResult);
                  $(".series-detail").attr("id",show);
                  $(".list_region_series .list .spinner").addClass("hide");
                  show_series_details();
              }
      });
    }
  });



  /* display movie_items  */
  function show_movies(){
    if ($(".list_region_movies .list .items .item").length > 0){
      $(".list_region_movies").removeClass("hide");
    } 
    else {
      $.ajax({
          type: "post",
          url: "movies_list/",
          data: {"list":"movies"},
          success: function(Data){
                  var str = "";
                  for(i=0;i<Data.length;i++){
                    var templateRawText = $("#movies_list").html();
                    var compiledTemplate = _.template(templateRawText);
                    var templateResult = compiledTemplate({name:"titanic","id":123,"year":1994});
                    $(".display_items .list_region_movies .list .items").html(templateResult);
                    str += listHTML;
                  }
                  $(".display_items .list_region_movies .list .items").html(listHTML);
                }
      });
    }
  }
  
/* series_list */
  function show_series(){
    if ($(".list_region_series .list .items .item").length > 0){
      $(".list_region_series").removeClass("hide");
      }
    else{
      $.ajax({
             type: "post",
             url: "series_list/",
             data: {"list":"series"},
             success: function(Data){
                     var str = "";
                     for(i=0;i<Data.length;i++){
                       var templateRawText = $("#series_list").html();
                       var compiledTemplate = _.template(templateRawText);
                       var templateResult = compiledTemplate({name:"titanic","id":123,"year":1994});
                       $(".display_items .list_region_series .list .items").html(templateResult);
                       str += listHTML;
                     } 
                     $(".display_items .list_region_series .list .items").html(listHTML);
                     $(".list_region_series").removeClass("hide");
                   }
      });
    }
  }
  var templateRawText = $("#movies_list").html();
  var compiledTemplate = _.template(templateRawText);
  var templateResult = compiledTemplate({name:"titanic","id":123,"year":1994});
  $(".display_items .list_region_movies .list .items").html(templateResult);
 // $(".display_items .list_region_series .list .items").html(templateResult); 
 });
