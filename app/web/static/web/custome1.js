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
        type: "get",
        url: "movies/"+id+"/",
        success: function(Data){
                 if ( Data.error == 0){
                   var templateRawText = $("#show_movie_details").html();
                   var compiledTemplate = _.template(templateRawText);
                   var templateResult = compiledTemplate({"movie":Data.data.name,"year":Data.data.year_of_release,"duration":Data.data.duration,"genre":Data.data.genre,"synopsis":Data.data.synopsys,"div":div_id});
                   var x = $(templateResult);
                   $("#mv").append(x);
                   $(".list_region_movies .spinner").addClass("hide");
  
                   show_movie_details();
                   availability(id);
                   }
                 else{
                   $(".list_region_movies .spinner").addClass("hide");
                   alert("movie data is not available");
                   }
              }
      });
    }
  }

/* function to get the availability */
  function availability(id){
    $.ajax({
        type: "get",
        url: "availability/"+id+"/",
        success: function(responseData){
          if ( responseData.error == 0){ 
            var templateRawText = $("#availability_script").html()
            var compiledTemplate = _.template(templateRawText);
            var templateResult = compiledTemplate({"avail":responseData.data.availability.platform_availabilities});
            var x = $(templateResult);
            $(".loading_avail").hide();
            $(".availability").append(x);
            }
          else{
              alert("availability not available");
              $(".loading_avail h1").text("data not available");
            }
          }
        });

  }
  /*series details */
  $("body").on("click",".list_region_series .item",function(){
    var id = parseInt($(this).attr("data-id"));
    var year = $(this).children().eq(3).text();
    series_details(id,year);
  });
  function series_details(id,year){
    var show = "#details"+"_"+id;
    var div_id = "details"+"_"+id;
    if( $(show).length > 0){
      $(show).removeClass("hide");
      }
    else{
      $(".list_region_series .spinner").removeClass("hide");
      $.ajax({
        type: "get",
        url: "tvseries/"+id+"/",
        success: function(Data){
          var templateRawText = $("#series_detail").html();
          var compiledTemplate = _.template(templateRawText);
          var templateResult = compiledTemplate({"name":Data.data.name,"year":year,"synopsys":Data.data.synopsis,"div":div_id,"genre":Data.data.genre,"season":Data.data.seasons});
          var x = $(templateResult);
          $(".list_region_series .spinner").addClass("hide");
          $("#sr").append(x);
          show_series_details();
          }
        });
      }
    } 



  /* display movie_items  */
  function show_movies(){
    if ($(".list_region_movies .list .items .item").length > 0){
      myFunction();
      $(".list_region_movies").removeClass("hide");
    } 
    else {
      $(".list_region_movies .spinner").removeClass("hide");
      $.ajax({
          type: "get",
          url: "movies/hot/",
          success: function(Data){
                  var str = " ";
                  var i;
                  if ( Data.error == 0){
                    for(i=0;i<Data.movies.length;i++){
                      var templateRawText = $("#movies_list").html();
                      var compiledTemplate = _.template(templateRawText);
                      var templateResult = compiledTemplate({name:Data.movies[i].name,"id":Data.movies[i].id,"year":Data.movies[i].year});
                      str += templateResult;
                    }
                    $(".list_region_movies .spinner").addClass("hide");
                    $(".display_items .list_region_movies .list .items").html(str);
                    myFunction();
                  }
                  else{
                    $(".list_region_movies .spinner").addClass("hide");
                    alert("data is not available");
                    }
                }
      });
    }
  }
  
/* series_list */
  function show_series(){
    if ($(".list_region_series .list .items .item").length > 0){
      myFunction();
      $(".list_region_series").removeClass("hide");
      }
    else{
      $(".list_region_series .spinner").removeClass("hide");
      $.ajax({
             type: "get",
             url: "tvseries/hot/",
             success: function(Data){
                     var str = "";
                     var i;
                     if ( Data.error == 0){
                       for(i=0;i<Data.series.length;i++){
                         var templateRawText = $("#series_list").html();
                         var compiledTemplate = _.template(templateRawText);
                         var templateResult = compiledTemplate({name:Data.series[i].name,"id":Data.series[i].id,"year":Data.series[i].year});
                         str += templateResult;
                         }
                       $(".list_region_series .spinner").addClass("hide");
                       $(".display_items .list_region_series .list .items").html(str);
                       myFunction();
                       $(".list_region_series").removeClass("hide");
                       }
                     else{
                       $(".list_region_series").removeClass("hide");
                       alert("data is not available");
                       }
                   }
      });
    }
  }

  /*    Episode details */
   $("body").on("click",".tab-episode",function(){
     var id = parseInt($(this).attr("data-id"));
     episode_details(id);
   });
   function episode_details(id){
     var show = "#episode_"+id;
     if ($(show).length>0){
       $(show).removeClass("hide");
       }
     else{
       $.ajax({
       type:"get",
       url:"episode/"+id+"/",
       success:function(Data){
           console.log(Data.name);
            var templateRawText = $("#episode_detail").html();
            var compiledTemplate = _.template(templateRawText);
            var templateResult = compiledTemplate({"title":Data.name,"genre":Data.genre,"lang":Data.language,"synopsys":Data.synopsis,"duration":Data.duration,"year":Data.year,"id":id});
            }
       });
     }
   }
 });


