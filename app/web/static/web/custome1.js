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
      $(".movie-detail").removeClass("hide");
  }

  $("body").on("click",".close-icon",function(){
    $(".movie-detail").addClass("hide");
    $(".shows-container-contain").addClass("hide");
  });

  function show_series_details(){
    $(".shows-container-contain").removeClass("hide");
  }
  $(".shows-container-contain > .close-icon").on("click",function(){
    $(".shows-container-contain").addClass("hide");
  });

  $("body").on("click",".nav.nav-hor.left",function(){
    $("#movie-detail").addClass("hide");
    $(".shows-container-contain").addClass("hide");
  });



 /* movie  details */

  $("body").on("click", ".list_region_movies .item",function(){
    console.log("click");
    var id = parseInt($(this).attr("data-id"));
    movie_details(id);
  });


  function movie_details(id){
    var show = "#details"+"_"+id;
    var div_id = "details"+"_"+id;
    if ( $(show).length > 0){
      $(show).removeClass("hide");
      }
    else{
      $(".list_region_movies .spinner").removeClass("hide");
      $.ajax({
        type: "post",
        url: "movies/"+id+"/",
        data: { "send_data":id,
              },
        success: function(Data){
                 console.log("success");
                 var templateRawText = $("#show_movie_details").html();
                 var compiledTemplate = _.template(templateRawText);
                 var templateResult = compiledTemplate({"movie":Data.name,"year":Data.year_of_release,"duration":Data.duration,"genre":Data.genre,"synopsis":Data.synopsys,"div":div_id});
                 var x = $(templateResult);
                 $("#mv").append(x);
                 $(".list_region_movies .spinner").addClass("hide");
                 console.log(templateResult);

                 show_movie_details();
              }
      });
    }
  }
  /*series details */
  $("body").on("click",".list_region_series .item",function(){
    var id = parseInt($(this).attr("data-id"));
    console.log(id)
    series_details(id);
  });
  function series_details(id){
    var show = "#details"+"_"+id;
    var div_id = "details"+"_"+id;
    if( $(show).length > 0){
      $(show).removeClass("hide");
      }
    else{
      $(".list_region_series .spinner").removeClass("hide");
      $.ajax({
        type: "post",
        url: "tvseries/"+id+"/",
        data: { "send_data":id,
              },
        success: function(Data){
          console.log("success");
          console.log(Data);
          var templateRawText = $("#series_detail").html();
          var compiledTemplate = _.template(templateRawText);
          var templateResult = compiledTemplate({"name":Data.name,"synopsys":Data.synopsis,"div":div_id,"genre":Data.genre});
          var x = $(templateResult);
          $(".list_region_series .spinner").addClass("hide");
          $("#sr").append(x);
          show_series_details();
          console.log(x);
          }
        });
      }
    } 



  /* display movie_items  */
  function show_movies(){
    if ($(".list_region_movies .list .items .item").length > 0){
      $(".list_region_movies").removeClass("hide");
    } 
    else {
      $(".list_region_movies .spinner").removeClass("hide");
      $.ajax({
          type: "post",
          url: "movies/hot/",
          data: {"list":"movies"},
          success: function(Data){
                  var str = " ";
                  var i;
                  for(i=0;i<Data.length;i++){
                    var templateRawText = $("#movies_list").html();
                    var compiledTemplate = _.template(templateRawText);
                    var templateResult = compiledTemplate({name:Data[i].name,"id":Data[i].id,"year":Data[i].year});
                    str += templateResult;
                  }
                  $(".list_region_movies .spinner").addClass("hide");
                  $(".display_items .list_region_movies .list .items").html(str);
                }
      });
    }
    console.log("movies shown");
  }
  
/* series_list */
  function show_series(){
    if ($(".list_region_series .list .items .item").length > 0){
      $(".list_region_series").removeClass("hide");
      }
    else{
      $(".list_region_series .spinner").removeClass("hide");
      $.ajax({
             type: "post",
             url: "tvseries/hot/",
             data: {"list":"series"},
             success: function(Data){
                     var str = "";
                     var i;
                     for(i=0;i<Data.length;i++){
                       var templateRawText = $("#series_list").html();
                       var compiledTemplate = _.template(templateRawText);
                       var templateResult = compiledTemplate({name:Data[i].name,"id":Data[i].id,"year":Data[i].year});
                       str += templateResult;
                     }
                     $(".list_region_series .spinner").addClass("hide");
                     $(".display_items .list_region_series .list .items").html(str);
                     $(".list_region_series").removeClass("hide");
                   }
      });
    }
    console.log("series shown");
  }
//  var templateRawText = $("#movies_list").html();
//  var compiledTemplate = _.template(templateRawText);
//  var templateResult = compiledTemplate({name:"titanic","id":123,"year":1994});
//  $(".display_items .list_region_movies .list .items").html(templateResult);
 // $(".display_items .list_region_series .list .items").html(templateResult);
  myFunction();

 });
