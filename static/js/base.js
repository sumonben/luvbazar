  // When the user scrolls down 50px from the top of the document, resize the header's font size
    window.onscroll = function() {
        scrollFunction()
    };

    function scrollFunction() {
        if (document.body.scrollTop >= 50 || document.documentElement.scrollTop >= 50) {
            document.getElementById("top-strip").className = "header sticky";
            document.getElementById("midilehead").className = "header sticky";
            document.getElementById("nav").className = "header sticky navbar navbar-expand-lg navbar-dark green-bg pt-1 pb-1";

        } else {
            document.getElementById("top-strip").className = "top-strip";
            document.getElementById("midilehead").className = "midilehead";
            document.getElementById("nav").className = "navbar navbar-expand-lg navbar-dark green-bg pt-1 pb-1";

        }
    }
   
   
     
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/63b6bbc8c2f1ac1e202bd8b0/1gm0sr2ki';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();

   

    
     
$(".close-btn").click(function(){
  $(".custom-model-main").removeClass('model-open');
});
$(".custom-model-main").addClass('model-open');


     
   $(document).ready(function () {
$('#myModal').modal('show');
}); 

     

//  $(document).ready(function () {
    
//     // Check if user saw the modal
//     var key = 'hadModal',
//         hadModal = localStorage.getItem(key);

//     // Show the modal only if new user
//     if (!hadModal) {
// 	setTimeout(function(){
        
// 		},3000);
//     }

	

//     // If modal is displayed, store that in localStorage
//      $("#closemodal").click(function(){
//         localStorage.setItem(key, true);
//     });
//     $("body").click(function(event) {
//         console.log(event.target.id);
//   if (event.target.id == "myModal") {
//     localStorage.setItem(key, true);
//   }
// });
// });


function verify_mobile_otp(){
    
    $.ajax({
                    /* the route pointing to the post function */
                    url: '/verify-mobile-otp',
                    type: 'POST',
                    /* send the csrf-token and the input to the controller */
                    data: {_token: '5Nal4ESjYMlHgXA3iFHsUYfFa6AbpNuNSU7RURFT', mobile:$("#bulkmobile").val(), otp:$("#mobile_otp").val()},
                    dataType: 'JSON',
                    /* remind that 'data' is the response of the AjaxController */
                    success: function (response) { 
                        var res=response.data.status;
                        var msg=response.data.message;
                       if(res == false)
                       {
                    $('#mobile_otp_mis').css("border", "1px solid red"); 
                    
                    
                    $('.mobile_otp_mis').removeClass("d-none").addClass("d-block");
                    
                    
                    $('.mobile_otp_mis').text(msg);
                    
                    
                    $('#mobile_otp').val('');     
                    $('.loginUrl').attr("action","#");
                    $('.btnMobile').attr('disabled',true);
                    $('.btnMobile').attr('type','button');
                       }
                       else
                       {
                     $('#mobile_otp').css("border", "1px solid green"); 
                    
                    
                    $('.mobile_otp_mis').removeClass("d-none").addClass("d-block");
                    
                    $('.mobile_otp_mis').css('color', 'green');
                    
                    $('.mobile_otp_mis').text("OTP has been verified successfully ");
                    $('.loginUrl').attr("action","https://www.ebookselibrary.com/submit-bulk-enquiry");
                    $('.btnMobile').attr('disabled',false);
                    $('.btnMobile').attr('type','submit');
                       }
                    
                    }
                });

}


     function checkmobilebulk(sel)
{


     // alert(data);


    var phone_number = sel.value;  


     //alert(phone_number);


      if(phone_number.length!=10){


     $('.message').text('(Mobile no. should be of 10 digits only)');


     $('.message').removeClass("d-none").addClass("d-block");


     $('.message').show();





      $('#bulkmobile').val('');


      $('#bulkmobile').css("border", "1px solid red");


        


    }
    else{
          $('.message').removeClass("d-block").addClass("d-none");


      $('.message').hide();


      //$('#phone_no').val('');


      $('#bulkmobile').css('border','');
      console.log(phone_number);
        $.ajax({
                    /* the route pointing to the post function */
                    url: '/send-mobile-otp',
                    type: 'POST',
                    /* send the csrf-token and the input to the controller */
                    data: {_token: '5Nal4ESjYMlHgXA3iFHsUYfFa6AbpNuNSU7RURFT', mobile:phone_number},
                    dataType: 'JSON',
                    /* remind that 'data' is the response of the AjaxController */
                    success: function (response) { 
                        var res=response.data.status;
                        if(res == 'success')
                       {
                       $('#mobileotpdiv').show();
                       $('.mobile_otp_mis').css('display','none');
                       $('.btnMobile').attr('disabled',true);
                       $('.btnMobile').attr('type','button');
                       $('#mobile_otp').val('');
                       }
                       else
                       {
                           var msg=response.data.message;
                $('.message').text(msg);
                
                $('.message').removeClass("d-none").addClass("d-block");
                
                $('.message').show();
                
                $('#bulkmobile').css("border", "1px solid red");    
                       }
                     
                    }
                });

    }





  }
  
 function verify_otp(){
    
    $.ajax({
                    /* the route pointing to the post function */
                    url: '/verify-email-otp',
                    type: 'POST',
                    /* send the csrf-token and the input to the controller */
                    data: {_token: '5Nal4ESjYMlHgXA3iFHsUYfFa6AbpNuNSU7RURFT', email:$("#bulkemail").val(), otp:$("#email_otp").val()},
                    dataType: 'JSON',
                    /* remind that 'data' is the response of the AjaxController */
                    success: function (response) { 
                        var res=response.data.status;
                        var msg=response.data.message;
                       if(res == false)
                       {
                    $('#email_otp').css("border", "1px solid red"); 
                    
                    
                    $('.email_otp_mis').removeClass("d-none").addClass("d-block");
                    
                    
                    $('.email_otp_mis').text(msg);
                    
                    
                    $('#email_otp').val('');     
                       }
                       else
                       {
                     $('#email_otp').css("border", "1px solid green"); 
                    
                    
                    $('.email_otp_mis').removeClass("d-none").addClass("d-block");
                    
                    $('.email_otp_mis').css('color', 'green');
                    
                    $('.email_otp_mis').text("OTP has been verified successfully ");
                       }
                    
                    }
                });

}


function testemail2(){


        


      var email=  $('#bulkemail').val();


      var _token = $('input[name="_token"]').val();


  


 // alert(email);


 if (validateEmail(email)) {


         $.ajax({
                    /* the route pointing to the post function */
                    url: '/send-email-otp',
                    type: 'POST',
                    /* send the csrf-token and the input to the controller */
                    data: {_token: '5Nal4ESjYMlHgXA3iFHsUYfFa6AbpNuNSU7RURFT', email:$("#bulkemail").val()},
                    dataType: 'JSON',
                    /* remind that 'data' is the response of the AjaxController */
                    success: function (response) { 
                       $('#otpdiv').show();
                        $('.email_mis').removeClass("d-block").addClass("d-none");


          $('#bulkemail').css("border", ""); 


          $('.email_mis').text("");
                     
                    }
                });
        

  } else {

      $('#bulkemail').css("border", "1px solid red"); 


         $('.email_mis').removeClass("d-none").addClass("d-block");


         $('.email_mis').text("(In valid Email)");


         $('#bulkemail').val(''); 


  }

} 

 function validateEmail(email) {


  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;


  return re.test(email);


}

     



    $(document).ready(function () {



   $("#opensearch").click(function(){



    $("#m-b-show").toggleClass("m-d-block w-100 mb-1")



   });



   });





     







$(document).ready(function () {



    $('.navbar-light .dmenu').hover(function () {



            $(this).find('.sm-menu').first().stop(true, true).slideDown(150);



        }, function () {



            $(this).find('.sm-menu').first().stop(true, true).slideUp(105)



        });



    }); 



     



        $(document).ready(function() {



        $(".megamenu").on("click", function(e) {



            e.stopPropagation();



        });



    });



    





     



  $(document).ready(function(){



      // Add minus icon for collapse element which is open by default



      $(".collapse.show").each(function(){



        $(this).prev(".card-header").find(".fa").addClass("fa-minus").removeClass("fa-plus");



      });



      



      // Toggle plus minus icon on show hide of collapse element



      $(".collapse").on('show.bs.collapse', function(){



        $(this).prev(".card-header").find(".fa").removeClass("fa-plus").addClass("fa-minus");



      }).on('hide.bs.collapse', function(){



        $(this).prev(".card-header").find(".fa").removeClass("fa-minus").addClass("fa-plus");



      });



  });






     



  



    jQuery("#banner-inner-slider").owlCarousel({



 autoplay: false,



 lazyLoad: true,



 loop: true,



 margin: 15,



  /*



 animateOut: 'fadeOut',



 animateIn: 'fadeIn',



 */



 responsiveClass: true,



 autoHeight: true,



 autoplayTimeout: 7000,



 smartSpeed: 800,



 nav: true,



 responsive: {



   0: {



     items: 4



   },







   600: {



     items: 3



   },







   1024: {



     items: 5



   },







   1366: {



     items: 7



   }



 }



});



        





     



  



  jQuery("#carousel3").owlCarousel({



 autoplay: true,



 lazyLoad: true,



 loop: true,



 margin: 20,



  /*



 animateOut: 'fadeOut',



 animateIn: 'fadeIn',



 */



 responsiveClass: true,



 autoHeight: true,



 autoplayTimeout: 7000,



 smartSpeed: 800,



 nav: true,



 responsive: {



   0: {



     items: 2



   },







   600: {



     items: 3



   },







   1024: {



     items: 4



   },







   1366: {



     items: 5



   }



 }



});



         





    

 


// 			AOS.init({



// 				easing: 'ease-out-back',



// 				duration: 1000



// 			});



		

     



			hljs.initHighlightingOnLoad();







			$('.hero__scroll').on('click', function(e) {



				$('html, body').animate({



					scrollTop: $(window).height()



				}, 1200);



			});



    

     







"use strict"; // Start of use strict



(function($) {











    function bootstrapAnimatedLayer() {







        function doAnimations(elems) {



            //Cache the animationend event in a variable



            var animEndEv = "webkitAnimationEnd animationend";







            elems.each(function() {



                var $this = $(this),



                    $animationType = $this.data("animation");



                $this.addClass($animationType).one(animEndEv, function() {



                    $this.removeClass($animationType);



                });



            });



        }







        //Variables on page load



        var $myCarousel = $("#minimal-bootstrap-carousel"),



            $firstAnimatingElems = $myCarousel



            .find(".carousel-item:first")



            .find("[data-animation ^= 'animated']");







        //Initialize carousel



        $myCarousel.carousel();







        //Animate captions in first slide on page load



        doAnimations($firstAnimatingElems);







        //Other slides to be animated on carousel slide event



        $myCarousel.on("slide.bs.carousel", function(e) {



            var $animatingElems = $(e.relatedTarget).find(



                "[data-animation ^= 'animated']"



            );



            doAnimations($animatingElems);



        });



    }







    bootstrapAnimatedLayer();















})(jQuery);





























     



    $(document).ready(function(){



      $("#ex1").zoom({



          magnify:1



      });



      $("#ex2").zoom();



      $("#ex3").zoom();



      $("#ex4").zoom();



      $("#ex5").zoom();



      $("#ex6").zoom();



    });



  

     



  function openCity(evt, cityName) {



  // Declare all variables



  var i, tabcontent, tablinks;







  // Get all elements with class="tabcontent" and hide them



  tabcontent = document.getElementsByClassName("tabcontent");



  for (i = 0; i < tabcontent.length; i++) {



    tabcontent[i].style.display = "none";



  }







  // Get all elements with class="tablinks" and remove the class "active"



  tablinks = document.getElementsByClassName("tablinks");



  for (i = 0; i < tablinks.length; i++) {



    tablinks[i].className = tablinks[i].className.replace(" active", "");



  }







  // Show the current tab, and add an "active" class to the link that opened the tab



  document.getElementById(cityName).style.display = "block";



  evt.currentTarget.className += " active";



}





     



$('.demo').accordionortabs();





     



   // tabbed content



    // http://www.entheosweb.com/tutorials/css/tabs.asp



    $(".tab_content").hide();



    $(".tab_content:first").show();







  /* if in tab mode */



    $("ul.tabs li").click(function() {



    



      $(".tab_content").hide();



      var activeTab = $(this).attr("rel"); 



      $("#"+activeTab).fadeIn();    



    



      $("ul.tabs li").removeClass("active");



      $(this).addClass("active");







    $(".tab_drawer_heading").removeClass("d_active");



    $(".tab_drawer_heading[rel^='"+activeTab+"']").addClass("d_active");



    



    });



  /* if in drawer mode */



  $(".tab_drawer_heading").click(function() {



      



      $(".tab_content").hide();



      var d_activeTab = $(this).attr("rel"); 



      $("#"+d_activeTab).fadeIn();



    



    $(".tab_drawer_heading").removeClass("d_active");



      $(this).addClass("d_active");



    



    $("ul.tabs li").removeClass("active");



    $("ul.tabs li[rel^='"+d_activeTab+"']").addClass("active");



    });



  



  



  /* Extra class "tab_last" 



     to add border to right side



     of last tab */



  $('ul.tabs li').last().addClass("tab_last");



  





     



jQuery("#por-slider,#por-slider-1").owlCarousel({



 autoplay: true,



 lazyLoad: true,



 loop: true,



 margin: 5,



 responsiveClass: true,



 autoHeight: true,



 autoplayTimeout: 7000,



 smartSpeed: 800,



 nav: true,



 responsive: {



   0: {



     items: 4,



     nav: false,



     dots: false



   },







   600: {



     items: 3,



     nav: false,



     dots: false



   },







   1024: {



     items: 4,



     nav: false,



     dots: false



   },







   1366: {



     items: 4



   }



 }



});





     



  $('#bookanyslider').owlCarousel({



    navigation : true,



    singleItem : true,



    transitionStyle : "fade",







    animateOut: 'fadeOut',



    animateIn: 'flipInX',



    items:1,



    margin:30,



    autoplay:true,



    stagePadding:30,



    smartSpeed:150,



    slideSpeed : 150,



    paginationSpeed : 400,



    autoplaySpeed:150,



     responsive: {



   0: {



     items: 1



   },







   600: {



     items: 1



   },







   1024: {



     items: 1



   },







   1366: {



     items: 1



   }



 }



});





     







  function testemail(){



      var id = jQuery(this).attr('value');



    // alert(id);







      var email=  $(this).val();



      var _token = $('input[name="_token"]').val();



  



//   alert(email);



 if (validateEmail(email)) {



    $.ajax({



    url:"/test/email",



    method:"POST",



    data:{email:email,_token:_token},



    success:function(result)



    {



     



     if(result==1){



         $('#email').css("border", "1px solid red"); 



         $('.email_mis').removeClass("d-none").addClass("d-block");



         $('.email_mis').text("(email id already taken)");



         $('#email').val(''); 



     }else{



         $('.email_mis').removeClass("d-block").addClass("d-none");



          $('#email').css("border", ""); 



          $('.email_mis').text("");



     }



    



    }







   });



 



 



 



  } else {



   



      $('#email').css("border", "1px solid red"); 



         $('.email_mis').removeClass("d-none").addClass("d-block");



         $('.email_mis').text("(In valid Email)");



         $('#email').val(''); 



   



   



  }



      



        







  }







    











 function validateEmail(email) {



  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;



  return re.test(email);



}



 function enterpassword(pas){



        



        var p=pas.value;



        //alert(p);



                errors = [];



    if (p.length < 6) {



        errors.push("Your password must be at least 6 characters");



         $('.mis_pass').removeClass("d-none").addClass("d-block");



         $('.mis_pass').text("Your password must be at least 6 characters");



         



         $('#password').css("border", "1px solid red");



    }



    if (p.search(/[a-z]/) < 0) {



        errors.push("Your password must contain at least one letter in lower case."); 



        $('.mis_pass').removeClass("d-none").addClass("d-block");



        $('.mis_pass').text("Your password must contain at least one letter in lower case.");



         $('#password').css("border", "1px solid red");



    }



     if (p.search(/[A-Z]/) < 0) {



        errors.push("Your password must contain at least one letter in upper case."); 



        $('.mis_pass').removeClass("d-none").addClass("d-block");



         $('.mis_pass').text("Your password must contain at least one letter in upper case.");



          $('#password').css("border", "1px solid red");



    }



      if (p.search(/[!@#$%^&*+-]/) < 0) {



        errors.push("Your password must contain at least one special character."); 



        $('.mis_pass').removeClass("d-none").addClass("d-block");



        $('.mis_pass').text("Your password must contain at least one special character.");



         $('#password').css("border", "1px solid red");



    }



    if (p.search(/[0-9]/) < 0) {



        $('.mis_pass').removeClass("d-none").addClass("d-block");



        $('.mis_pass').text("Your password must contain at least one digit.");



        errors.push("Your password must contain at least one digit.");



         $('#password').css("border", "1px solid red");



    }



    if (errors.length > 0) {



       // alert(errors.join("\n"));



       $('.mis_pass').removeClass("d-none").addClass("d-block");



          $('#password').val('');



             return false;



    }else{



        $('.mis_pass').removeClass("d-block").addClass("d-none");



        $('.mis_pass').hide();



        



        $('#password').css('border','');



         return true;



    }



    }











     function checkmobile(sel)



{



     // alert(data);



    var phone_number = sel.value;  



     //alert(phone_number);



      if(phone_number.length!=10){







     $('.message').text('(Mobile no. should be of 10 digits only)');



     $('.message').removeClass("d-none").addClass("d-block");



     $('.message').show();







      $('.mobile').val('');



      $('.mobile').css("border", "1px solid red");



        



    }else{



      $('.message').removeClass("d-block").addClass("d-none");



      $('.message').hide();



      //$('#phone_no').val('');



      $('.mobile').css('border','');







    }







  }



















  function add_to_cart(book_id){







   toastr.success('book added to cart');







  }







  function check_life_time(){



    toastr.success('check life time');







  }



  function check_one_year(){



    toastr.success('check one year');







  }



  function check_six_month(){



    toastr.success('check six month');







  }























//   function add_book_to_cart_no_login(){







//     alert('Login First then You able to add this book to your cart');



//   }



  



  



  



  $(document).ready(function () {



 



window.setTimeout(function() {



    $(".alert").fadeTo(1000, 0).slideUp(1000, function(){



        $(this).remove(); 



    });



    



   // $('.alert2').css('display','none');



}, 5000);



window.setTimeout(function() {



   



   



   



}, 5000);



});















function apply_price_filter(){



     $('#book_loader').css('display','block');



    var range_start=$('#range_start').val();



    var range_end=$('#range_end').val();



    var cat_id=$('#page_cat_id').val();



    var sub_cat_id=$('#page_sub_cat_id').val();



        $.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/price_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{range_start:range_start,range_end:range_end,cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



       



        $("#myModal1").modal('hide');



      $('#book_list').html(data);



      



  }



     



  });



}







function apply_price_filter_new(){



     $('#book_loader').css('display','block');



    var range_start=$('#range_start2').val();



    var range_end=$('#range_end2').val();



    var cat_id=$('#page_cat_id2').val();



    var sub_cat_id=$('#page_sub_cat_id2').val();



        $.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/price_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{range_start:range_start,range_end:range_end,cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



       



        $("#myModal1").modal('hide');



      $('#book_list').html(data);



      



  }



     



  });



}







   



        $(".radio_botton_filter").click(function(){



             var button_id=this.id;



        //   alert(button_id);



            //document.getElementById(button_id).checked = true;



            $("#"+button_id).prop("checked", true);



            $('#book_loader').css('display','block');



            var radioValue = $("input[name='customRadio']:checked").val();



             var cat_id=$('#page_cat_id').val();



              var sub_cat_id=$('#page_sub_cat_id').val();



              var search='';



              if($('#search_input').val() != '')



              {



                  search=$('#search_input').val();



              }



            if(radioValue){



           // alert(button_id);



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/addon_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{radioValue:radioValue,cat_id:cat_id,sub_cat_id:sub_cat_id,search_input:search},



    success:function(data)



  {



       $('#book_loader').css('display','none');



       $("#myModal").modal('hide');



       $('#book_list').html(data);



      



  }



     



  });   



   



               



               



               



            }



        });

        

        $(".radio_botton_filter_exam").click(function(){



             var button_id=this.id;



        //   alert(button_id);



            //document.getElementById(button_id).checked = true;



            $("#"+button_id).prop("checked", true);



            $('#book_loader').css('display','block');



            var radioValue = $("input[name='customRadio']:checked").val();



             var cat_id=$('#page_cat_id').val();



              var sub_cat_id=$('#page_sub_cat_id').val();



              var search='';



              if($('#keywordsall').val() != '')



              {



                  search=$('#keywordsall').val();



              }



            if(radioValue){



           // alert(button_id);



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/exam_addon_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{radioValue:radioValue,cat_id:cat_id,sub_cat_id:sub_cat_id,keywords:search},



    success:function(data)



  {



       $('#book_loader').css('display','none');



       $("#myModal").modal('hide');



       $('#book_list').html(data);



      



  }



     



  });   



   



               



               



               



            }



        });

    



 $(document).ready(function(){



        $(".radio_botton_filter_desktop").click(function(){



             var button_id=this.id;



           



            document.getElementById(button_id).checked = true;



            



            $('#book_loader').css('display','block');



            var radioValue = $("input[name='customRadio_desktop']:checked").val();



             var cat_id=$('#page_cat_id').val();



              var sub_cat_id=$('#page_sub_cat_id').val();



            if(radioValue){



          // alert(radioValue);



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/addon_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{radioValue:radioValue,cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



       $("#myModal").modal('hide');



       $('#book_list').html(data);



      



  }



     



  });   



   



               



               



               



            }



        });



    });



 $(document).ready(function(){



        $(".free_radio_botton_filter_desktop").click(function(){



            



            $('#book_loader').css('display','block');



            var radioValue = $("input[name='customRadio_desktop']:checked").val();



             var cat_id=$('#page_cat_id').val();



              var sub_cat_id=$('#page_sub_cat_id').val();



            //   alert(cat_id);



            if(radioValue){



               



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/free/addon_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{radioValue:radioValue,cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



      $('#book_list').html(data);



      



  }



     



  });   



   



               



               



               



            }



        });



    });



    



    



$(document).ready(function(){



        $(".radio_botton_filter_free").click(function(){



            



            $('#book_loader').css('display','block');



            var radioValue = $("input[name='customRadio']:checked").val();



             var cat_id=$('#page_cat_id').val();



              var sub_cat_id=$('#page_sub_cat_id').val();



            if(radioValue){



               



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/free/addon_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{radioValue:radioValue,cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



      $('#book_list').html(data);



      



  }



     



  });   



   



               



               



               



            }



        });



    });



    



    



     $(document).ready(function(){



        $(".p_radio_botton_filter").click(function(){



            



            $('#book_loader').css('display','block');



            var radioValue = $("input[name='customRadio']:checked").val();



            



             var p_id=$('#p_id').val();



             var cat_id=$('#page_cat_id_new').val();



              var sub_cat_id=$('#page_sub_cat_id_new').val();



            // alert(p_id);



            if(radioValue){



               



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/p_addon_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{radioValue:radioValue,p_id:p_id,cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



      $('#book_list').html(data);



      



  }



     



  });   



   



               



               



               



            }



        });



    });



    



    function place_order(){



        



        var total_price=$('#total_price').val();



        var tax=$('#tax').val();



        var payable=$('#payable').val();



        var buyer_id=$('#buyer_id').val();



        var cart_ids=$('#cart_id').val();



         var coupon_id = $("input[name='coupon_apply']:checked").val();



        



       $.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/place_order',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{total_price:total_price,tax:tax,payable:payable,buyer_id:buyer_id,cart_ids:cart_ids,coupon_id:coupon_id},



    success:function(data)



  {



      



    //  alert('ok');



    //   $('#book_loader').css('display','none');



    //   $('#book_list').html(data);



      



  }



     



  });      



        



        



        



        



    }



    



    function change_password_style(){



        



        var changed_value=$('#changed_value').text();



        if(changed_value=='password'){



            



             $('#login_password').prop('type','text');



             $('#changed_value').text('text');



        }



       



        if(changed_value=='text'){



            



             $('#login_password').prop('type','password');



             $('#changed_value').text('password');



        }



    }



    



     function change_password_style2(){



        



        var changed_value=$('#changed_value2').text();



        if(changed_value=='password'){



            



             $('#password').prop('type','text');



             $('#changed_value2').text('text');



        }



       



        if(changed_value=='text'){



            



             $('#password').prop('type','password');



             $('#changed_value2').text('password');



        }



    }











  

     



	    $(document).ready(function(){ 



	       $('#btnContactUs').click(function(){



	           



	           



	           var name=$('.name').val();



	           var email=$('.email').val();
	           var otp_text=$('.otp_text').val();



	           var phone=$('.phone').val();
	           var typeUser=$('.typeCls').val();



	           



	           var message=$('.comment').val();



	           



	           var _token = $('input[name="_token"]').val();



	           



	           if(name==''){



	               alert('Name field is required');



	           }
	           if(typeUser==''){



	               alert('Type field is required');



	           }



	           else if(email==''){



	               alert('Email field is required');



	           }
	           else if(otp_text==''){



	               alert('OTP field is required');



	           }



	           



	           else if(message==''){



	               alert('Message field is required');



	           }



	          //  else if(validateCaptcha() == false)



            //        {



            //            alert('Invalid Captcha. try Again');



            //        }



	           else{

              if(otp_text!=''){

                $.ajax({
                    type: "POST",
                    url: "https://www.ebookselibrary.com/validate-contact-otp",
                    data: { otp_text:otp_text, _token:_token},
                    cache: false,
                    success:function(reslt){
                      if(reslt == '1'){

                        $('#book_loader').css('display','block');

                            $.ajax({

                                  type: "POST",

                                  url: "https://www.ebookselibrary.com/submit-enquiry",

                                  data: { name:name,email:email,message:message,phone:phone,typeUser:typeUser, _token:_token},

                                  cache: false,

                                  success: function(result){

                                      $('#book_loader').css('display','none');

                                  alert(result);

                                    location.reload();

                                  }



                                  });

                      }else{
                        alert('Please enter valid OTP!')
                      }
                    }
                    });

                  }

	        

	           }



	           



	       }) ;



	    });



	    



	    $(document).ready(function(){



	        



	          



            //  $('#coupon_appied_section').css('display','none');



            //   $('#coupon_title').css('display','none');



            //  $('#applied_coupon_amount').css('display','none');



	        



	    });



	


     
    toastr.options = {
          closeButton: true,
          newestOnTop: false,
          progressBar: true,
          positionClass: "toast-top-right",
          preventDuplicates: false,
          onclick: null,
          showDuration: "300",
          hideDuration: "1000",
          timeOut: "5000",
          extendedTimeOut: "1000",
          showEasing: "swing",
          hideEasing: "linear",
          showMethod: "fadeIn",
          hideMethod: "fadeOut"
        };
    


     
    $(document).ready(function() {
      $('.nameUni').on('input', function() {
        var regex = /[^a-zA-Z.,\s]/g;
        if (this.value.match(regex)) {
          this.value = this.value.replace(regex, '');
          //console.log('mm');
        //   $('.name_regex').text('Special character not allowed in name. Allow only alphabets,comma(,), and dot(.)')
        toastr.error('Error', 'Please enter valid name. Only alphabets, comma(,) and dot(.) are allowed.', {timeOut: 8000})
        }
      });
    });

     
    $(document).ready(function() {
      $('.commentUni').on('input', function() {
        var regex = /[^a-zA-Z0-9.,\s]/g;
        if (this.value.match(regex)) {
          this.value = this.value.replace(regex, '');
          //console.log('mm');
        //   $('.name_regex').text('Special character not allowed in name. Allow only alphabets,comma(,), and dot(.)')
        toastr.error('Error', 'Please enter valid message. Only alphabets, numbers, comma(,) and dot(.) are allowed.', {timeOut: 8000})
        }
      });
    });


     







  



  function get_publisher_books(p_id,cat_id,sub_cat_id){



     var className = $('.addon_class').removeClass('sub_active');



  



  $('#p_id_list_'+p_id).toggleClass('sub_active');



  $('#p_id_list_desktop_'+p_id).toggleClass('sub_active');



       $('#book_loader').css('display','block');



            var p_id = p_id;



             var cat_id=cat_id;



              var sub_cat_id=sub_cat_id;



            



               



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/publisher_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{p_id:p_id,cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



       $("#myModal1").modal('hide');



      $('#book_list').html(data);



      



  }



     



  });   



   



        



  



  }



  



  



   function get_publisher_books_institute(p_id,cat_id,sub_cat_id){



     var className = $('.addon_class').removeClass('sub_active');



  



  $('#p_id_list_'+p_id).toggleClass('sub_active');



  $('#p_id_list_desktop_'+p_id).toggleClass('sub_active');



       $('#book_loader').css('display','block');



            var p_id = p_id;



             var cat_id=cat_id;



              var sub_cat_id=sub_cat_id;



            



               



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/institute/book/publisher_filter',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{p_id:p_id,cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



       $("#myModal1").modal('hide');



      $('#book_list').html(data);



      



  }



     



  });   



   



        



  



  }



	


     



  











  function add_book_to_cart_no_login(){



      



      



        Swal.fire({



        title: 'Login/Register first to  add book to your cart',



        html: "" +



            "<br>" +'<a href="https://www.ebookselibrary.com/user-login"><button type="button" role="button" tabindex="0" class="btn btn-outline-light m-auto orange-btn" style="margin-top:10px!important;">' + 'Login' + '</button></a>'+'<a href="https://www.ebookselibrary.com/register-user"><button type="button" role="button" tabindex="0" class="btn btn-outline-light m-auto orange-btn" style="margin-top:10px!important;margin-left:5px!important;">' + 'Register' + '</button></a>',



        showCancelButton: false,



        showConfirmButton: false



    });



      



     



   



  }



  



  



  



  $(document).ready(function () {



 



window.setTimeout(function() {



    $(".alert").fadeTo(1000, 0).slideUp(1000, function(){



        $(this).remove(); 



    });



}, 5000);



});























  

     



	 



	

     



function getVals(){



  // Get slider values



  var parent = this.parentNode;



  var slides = parent.getElementsByTagName("input");



    var slide1 = parseFloat( slides[0].value );



    var slide2 = parseFloat( slides[1].value );



    



    



  // Neither slider will clip the other, so make sure we determine which is larger



  if( slide1 > slide2 ){ var tmp = slide2; slide2 = slide1; slide1 = tmp; }



  



  var displayElement = parent.getElementsByClassName("rangeValues")[0];



      displayElement.innerHTML = "₹ " + slide1 + "Rs. - ₹ " + slide2 + "Rs.";



      



      



      $('#range_start').val(slide1);



      $('#range_end').val(slide2);



      



      $('#range_start2').val(slide1);



      $('#range_end2').val(slide2);



      



}







window.onload = function(){



  // Initialize Sliders



 // $('.range-slider').css('display','none');



  var sliderSections = document.getElementsByClassName("range-slider");



      for( var x = 0; x < sliderSections.length; x++ ){



        var sliders = sliderSections[x].getElementsByTagName("input");



        for( var y = 0; y < sliders.length; y++ ){



          if( sliders[y].type ==="range" ){



            sliders[y].oninput = getVals;



            // Manually trigger event first time to display values



            sliders[y].oninput();



          }



        }



      }



}





     



$("#vertical-menu h3").click(function () {



    //Inner 



    var jqInner = $(this).next();



    if (jqInner.is(":visible"))



    {



        jqInner.slideUp()



        $(this).find('span').html('+');



    }



    else



    {



        jqInner.slideDown()



        $(this).find('span').html('-');



    }



})





     



    $(document).ready(function(){



        $(".rent_type_choose").click(function(){



            var radioValue = $("input[name='rent_type']:checked").val();



            if(radioValue=='six_month'){



               



               var six_month_price=$('#six_month_selling_price').text();



               var six_month_discount=$('#six_month_discount').text();



               var original_book_price=$('#my_book_price').text();



               



               



               var total_saving=original_book_price-six_month_price;



               



              // var saving=parseFloat(total_saving).toFixed(2);



              



              var saving=roundNumberV1(total_saving,2);



             // alert(saving);



               



               $('#rent_total_price').text(six_month_price);



               $('#rent_actual_discount').text(six_month_discount);



               $('#rent_save').text(saving);



            }



            if(radioValue=='one_year'){



               



               var one_year_price=$('#one_year_selling_price').text();



               var one_year_discount=$('#one_year_price').text();



                var original_book_price=$('#my_book_price').text();



                 var total_saving=original_book_price-one_year_price;



                  var saving=roundNumberV1(total_saving,2);



                  



                //  alert(saving);



              //  var saving=parseFloat(total_saving).toFixed(2);



               $('#rent_total_price').text(one_year_price);



               $('#rent_actual_discount').text(one_year_discount);



               $('#rent_save').text(saving);



               // alert("Your are a - " + radioValue);



            }



        });



    });



    



    



    function roundNumberV1(num, scale) {



  if(!("" + num).includes("e")) {



    return +(Math.round(num + "e+" + scale)  + "e-" + scale);  



  } else {



    var arr = ("" + num).split("e");



    var sig = ""



    if(+arr[1] + scale > 0) {



      sig = "+";



    }



    var i = +arr[0] + "e" + sig + (+arr[1] + scale);



    var j = Math.round(i);



    var k = +(j + "e-" + scale);



    return k;  



  }



}





     



    jQuery("#carousel").owlCarousel({



 autoplay: true,



 lazyLoad: true,



 loop: true,



 margin: 20,



  /*



 animateOut: 'fadeOut',



 animateIn: 'fadeIn',



 */



 responsiveClass: true,



 autoHeight: true,



 autoplayTimeout: 7000,



 smartSpeed: 800,



 nav: true,



 responsive: {



   0: {



     items: 3



   },







   600: {



     items: 3



   },







   1024: {



     items: 6



   },







   1366: {



     items: 6



   }



 }



});





     



    jQuery("#carousel1").owlCarousel({



 autoplay: true,



 lazyLoad: true,



 loop: true,



 margin: 20,



  /*



 animateOut: 'fadeOut',



 animateIn: 'fadeIn',



 */



 responsiveClass: true,



 autoHeight: true,



 autoplayTimeout: 7000,



 smartSpeed: 800,



 nav: true,



 responsive: {



   0: {



     items: 3



   },







   600: {



     items: 3



   },







   1024: {



     items: 6



   },







   1366: {



     items: 6



   }



 }



});





     



    jQuery("#carousel2").owlCarousel({



 autoplay: true,



 lazyLoad: true,



 loop: true,



 margin: 20,



  /*



 animateOut: 'fadeOut',



 animateIn: 'fadeIn',



 */



 responsiveClass: true,



 autoHeight: true,



 autoplayTimeout: 7000,



 smartSpeed: 800,



 nav: true,



 responsive: {



   0: {



     items: 3



   },







   600: {



     items: 3



   },







   1024: {



     items: 6



   },







   1366: {



     items: 6



   }



 }



});




    <iframe allow="join-ad-interest-group" data-tagging-id="AW-11366204248" data-load-time="1716621214281" height="0" width="0" src="https://td.doubleclick.net/td/rul/11366204248?random=1716621214256&amp;cv=11&amp;fst=1716621214256&amp;fmt=3&amp;bg=ffffff&amp;guid=ON&amp;async=1&amp;gtm=45je45m0v9137502842z89176648053za200zb9176648053&amp;gcd=13l3l3l3l1&amp;dma=0&amp;u_w=1366&amp;u_h=768&amp;url=https%3A%2F%2Fwww.ebookselibrary.com%2F&amp;ref=https%3A%2F%2Fwww.ebookselibrary.com%2Fbook-detail%2Fgeneral%2Fstory-books%2FA-LITTLE-PRINCESS-645&amp;hn=www.googleadservices.com&amp;frm=0&amp;tiba=Ebooks%20Library%20Online%20%7C%20Free%20Ebooks%20for%20higher%20education&amp;npa=0&amp;pscdl=label_only_1&amp;auid=1274887756.1716608295&amp;uaa=x86&amp;uab=64&amp;uafvl=Google%2520Chrome%3B125.0.6422.77%7CChromium%3B125.0.6422.77%7CNot.A%252FBrand%3B24.0.0.0&amp;uamb=0&amp;uam=&amp;uap=Windows&amp;uapv=15.0.0&amp;uaw=0&amp;fledge=1&amp;data=event%3Dgtag.config" style="display: none; visibility: hidden;"></iframe>

     



   



    $(document).ready(function() {



        



        var isMobile = {



Android: function() {



return navigator.userAgent.match(/Android/i);



},



BlackBerry: function() {



return navigator.userAgent.match(/BlackBerry/i);



},



iOS: function() {



return navigator.userAgent.match(/iPhone|iPad|iPod/i);



},



Opera: function() {



return navigator.userAgent.match(/Opera Mini/i);



},



Windows: function() {



return navigator.userAgent.match(/IEMobile/i);



},



any: function() {



return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());



}



};



$(document).on("click", '.whatsapp', function() {



if( isMobile.any() ) {



var text = $(this).attr("data-text");



var url = $(this).attr("data-link");



var message = encodeURIComponent(text) + " - " + encodeURIComponent(url);



var whatsapp_url = "whatsapp://send?text=" + message;



window.location.href = whatsapp_url;



} else {



    



  var text = $(this).attr("data-text");



var url = $(this).attr("data-link");



var message = encodeURIComponent(text) + " - " + encodeURIComponent(url);



var whatsapp_url = "https://web.whatsapp.com/send?text=" + message;



window.location.href = whatsapp_url;  



    



//alert("Please share this article in mobile device");



}



});



});



      





     



    



    $(document).ready(function(){



     $("li .disabled").mouseover(function(){



   // $("p").css("background-color", "yellow");



    alert('feature not available');



  });



    });



  





     



//  $( '#submit_search' ).on( 'click', function() {







    



//  });



 



   $("#submit_search").on('click',function(e){



        e.preventDefault();



        



                 var cat_id = $('#state_list').children("option:selected").val();



         var search_input=$('#search_input').val();



        



         //alert(search_string);



        // if(cat_id!='' || search_input!=''){



            



        //     alert('both field are not empty');



        // }



    // alert(cat_id);



     $.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



}); 







 if(search_input!='' || (cat_id!='' || cat_id!=0)){



     $.ajax({



        type: "POST",



        url: '/filter/search_filter',



        data: { cat_id:cat_id, search_input:search_input }, 



        success: function( msg ) {



           if(msg=='0'){



               alert('No Match record');



           }else{



             $('#search_from').submit();  



               



           }



        }



        



    });



    



}else{



    



    alert('select atleast one category or enter any keyword');



}



        



    });



    





     



   



   



//       $(document).ready(function(){



           



//             if($('.use_wallet_amount').prop("checked") == true){



//               // console.log("Checkbox is checked.");



//               $('#coupon_appied_section').css('display','block');



//               $('#coupon_title').css('display','block');



//               $('#applied_coupon_amount').css('display','inline-block');



//               $('#new_payable_amount').css('display','inline-block');



//               // alert('checked');



//             }



//             else if($('.use_wallet_amount').prop("checked") == false){



//                 $('#coupon_appied_section').css('display','block');



//               $('#coupon_title').css('display','block');



//               $('#applied_coupon_amount').css('display','inline-block');



//               $('#new_payable_amount').css('display','inline-block');



//             }



            



//           var default_coupon_applied=$('#default_p_coupon_book').val();



//           var default_p_coupon_code=$('#default_p_coupon_code').val();



//           var coupon_applied_books=$('#coupon_applied_books').val();



//           if(coupon_applied_books!=''){



          



//           var a = default_coupon_applied.split(","),



//     i;











//     var book_price=$('#total_mrp').text();



//     var price_after_coupon_total_amount=$('#price_after_coupon_total_amount').text();



    



//     var total_saving=book_price-price_after_coupon_total_amount;



//      var gross_saving=total_saving.toFixed(2);



//     $('#total_saving').text(gross_saving);



//     // alert(gross_saving);



// for (i = 0; i < a.length; i++) {



    



//     var app_message='Coupon applied-'+default_p_coupon_code+'-'+a[i];



//     $('#publisher_coupon_applied_'+a[i]).text(app_message);



//     $('#publisher_coupon_applied_'+a[i]).css('display','block');



    



    



    



    



    



    



    



    



    



    



    



    



    



// }



      



//           }     



           



//       });



   



   



   



   



   



        $('.use_wallet_amount').click(function(){



            if($(this).prop("checked") == true){



              //  alert('checked');



               // console.log("Checkbox is checked.");



               



               var total_price=$('#total_payable').text();



               var wallet_available=$('#wallet_amount').text();



               var wallet_deduction=(total_price*10)/100;



                 var price_after_wallet=total_price-(total_price*10)/100;



                 



               if(wallet_available>wallet_deduction){



                   



                     $('#amount_payable').text(price_after_wallet);



                   



               }else{



                   



                      var changed_amount=total_price-wallet_available;



                   



                     $('#amount_payable').text(changed_amount);



               }



               



             



               



             



               



               



               



               



               



               



            }



            else if($(this).prop("checked") == false){



                  var total_price=$('#total_payable').text();



                  $('#amount_payable').text(total_price);



               // alert('not checked');



               // console.log("Checkbox is unchecked.");



            }



        });



   





     



  



     function change_password_style(){



        



       // alert('ok');



        var changed_value=$('#changed_value').text();



        if(changed_value=='password'){



            



             $('#old_password').prop('type','text');



             $('#changed_value').text('text');



        }



       



        if(changed_value=='text'){



            



             $('#old_password').prop('type','password');



             $('#changed_value').text('password');



        }



    }



    



     function change_password_style2(){



        



        var changed_value=$('#change_value_new').text();



        if(changed_value=='password'){



            



             $('#password').prop('type','text');



             $('#change_value_new').text('text');



        }



       



        if(changed_value=='text'){



            



             $('#password').prop('type','password');



             $('#change_value_new').text('password');



        }



    }



    



    function change_password_style3(){



        



         var changed_value=$('#change_value_new2').text();



        if(changed_value=='password'){



            



             $('#c_password').prop('type','text');



             $('#change_value_new2').text('text');



        }



       



        if(changed_value=='text'){



            



             $('#c_password').prop('type','password');



             $('#change_value_new2').text('password');



        }



        



    }











 function change_c_pass22(pas){







      var p=pas.value;



            



                errors = [];



    if (p.length < 6) {



        errors.push("At least 6 characters are required");



         $('.c_pass_mis').removeClass("d-none").addClass("d-block");



         $('.c_pass_mis').text("(At least 6 characters are required)");



         $('#c_password').val('');



         $('#c_password').css("border", "1px solid red");



    }



    if (p.search(/[a-z]/) < 0) {



        errors.push("(At least one letter in lower case is required.)"); 



        $('.c_pass_mis').removeClass("d-none").addClass("d-block");



        $('.c_pass_mis').text("(At least one letter in lower case is required.)");



        $('#c_password').val('');



         $('#c_password').css("border", "1px solid red");



    }



     if (p.search(/[A-Z]/) < 0) {



        errors.push("(At least one letter in upper case is required.)"); 



        $('.c_pass_mis').removeClass("d-none").addClass("d-block");



         $('.c_pass_mis').text("(At least one letter in upper case is required.)");



         $('#c_password').val('');



          $('#c_password').css("border", "1px solid red");



    }



      if (p.search(/[!@#$%^&*+-]/) < 0) {



        errors.push("(At least one special character is required.)"); 



        $('.c_pass_mis').removeClass("d-none").addClass("d-block");



        $('.c_pass_mis').text("(At least one special character is required.)");



        $('#c_password').val('');



         $('#c_password').css("border", "1px solid red");



    }



    if (p.search(/[0-9]/) < 0) {



        $('.c_pass_mis').removeClass("d-none").addClass("d-block");



        $('.c_pass_mis').text("(At least one digit is required.)");



        errors.push("(At least one digit is required.)");



        $('#c_password').val('');



         $('#c_password').css("border", "1px solid red");



    }



    if (errors.length > 0) {



      // alert(errors.join("\n"));



      $('.c_pass_mis').removeClass("d-none").addClass("d-block");



      $('#c_password').val('');



             return false;



    }else{



        



      var new_pass= $('#password').val();



    



       



      



      



     



      if(p!=new_pass){



          $('.c_pass_mis').removeClass("d-none").addClass("d-block");



         $('.c_pass_mis').text("(Confirm Password not Match with New Password)");  



         $('#c_password').val('');



           



      }else{



            $('.c_pass_mis').removeClass("d-block").addClass("d-none");



        $('.c_pass_mis').hide();



        



        $('#c_password').css('border','');



         return true;



           



      }



       



    }



    }



    











 $(document).ready(function(){



      $('#reader_change_password').on('submit', function(event){



        event.preventDefault();



   



  var _token = $('input[name="_token"]').val();



    $.ajax({



   url:'/reader/change_password',



   method:"POST",



   data:new FormData(this),



   dataType:'JSON',



   contentType: false,



   cache: false,



   processData: false,



   success:function(data)



   {



      



    if(data.status=='ok'){



       // alert('ok');



    $('#reset_pass_error').addClass(data.class_name);



    $('#reset_pass_error').text(data.message);







     $("#reset_pass_error").fadeTo(2000, 500).slideUp(500, function(){



                         $("#reset_pass_error").slideUp(500);



                         



                        // location.reload();



                        });



   // $('#profile_error').addClass(data.class_name);



    }if(data.status=='notok'){







      //alert('not ok');



    $('#reset_pass_error').removeClass("alert-success");   



    $('#reset_pass_error').addClass(data.class_name);



    $('#reset_pass_error').text(data.message);



    $("#reset_pass_error").fadeTo(2000, 500).slideUp(500, function(){



                         $("#reset_pass_error").slideUp(500);



                         



                        // location.reload();



                        });



    }



    



   }



     



  }); 



    



    



      });   



  }) ;



    





     



  $('#mobile-slider-top').owlCarousel({



    navigation : false,



    singleItem : true,



    items:1,



    margin:30,



    loop:true,



    autoplay:true,



    // stagePadding:30,



    smartSpeed:150,



    nav:false,



    slideSpeed : 150,



    paginationSpeed : 400,



    autoplaySpeed:150,



    dots:true,



     responsive: {



   0: {



     items: 1



   },







   600: {



     items: 1



   },







   1024: {



     items: 1



   },







   1366: {



     items: 1



   }



 }



});





     



    $('#click_on_view').click(function(){



        



       var fl_class= $('#view_icon').attr('class');



       if(fl_class=='fa fa-th-list'){



           



            $('#view_icon').removeClass('fa-th-list').addClass('fa-th-large');



       }else if(fl_class=='fa fa-th-large'){



           



            $('#view_icon').removeClass('fa-th-large').addClass('fa-th-list');



       }



     



        



    });



    



    $('#click_on_view').click(function(){



     



   $('.crd').toggleClass("add_card");



      



     



  });



  



  function reset_short_data(){



      



     document.querySelector('input[name="customRadio"]:checked').checked = false;



     



         $('#book_loader').css('display','block');



           // var radioValue = $("input[name='customRadio']:checked").val();



             var cat_id=$('#page_cat_id').val();



              var sub_cat_id=$('#page_sub_cat_id').val();



        



               



$.ajaxSetup({



    headers: {



        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')



    }



});    







  $.ajax({



  url:'/book/addon_filter_new2',



  method:"POST",



  headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},



  data:{cat_id:cat_id,sub_cat_id:sub_cat_id},



    success:function(data)



  {



       $('#book_loader').css('display','none');



       $("#myModal").modal('hide');



       $('#book_list').html(data);



      



  }



     



  });   



   



         



     



  }



  



  function reset_price_data(){



      



    window.location.reload();



  }





     



window.onload = function ()



{







    setTimeout(function(){ 



      //$("#flash_sale").show();



      $("#flash_sale").removeClass('slide-out-left d-none').addClass('slide-in-left d-block');



      



    }, 2000);



    



      setTimeout(function(){ 



          



//               var book_list=$('#top_selling_book_ids').val();



  



           



//           var books=book_list.split(',');







//             var rand_book= get_random(books);



            



//           var _token = $('input[name="_token"]').val();







//     $.ajax({



//     url:"/test/get_flash_sale",



//     method:"POST",



//      dataType: 'json',



//     data:{book_id:rand_book,_token:_token},



//     success:function(result)



//     {



     



//      $('#flash_title').text(result.title)



//      $('#flash_author').text(result.author)



//       $('#flash_img').attr('src',result.book_img);



    



//     }







//   });



          



          



          



          



      //$("#flash_sale").show();



      $("#flash_sale").removeClass('slide-in-left d-block').addClass('slide-out-left d-none');



      



    }, 12000);



};







function close_flash_sale(){



    



    $("#flash_sale").removeClass('slide-in-left d-block').addClass('slide-out-left d-none');



    



}

















     



var myVar;



setInterval(alertFunc, 10000);







setInterval(alertFunc2, 15000);







function alertFunc() {



          var book_list=$('#top_selling_book_ids').val();



           



           var books=book_list.split(',');



  var rand_book= get_random(books);







 var _token = $('input[name="_token"]').val();



    $.ajax({



    url:"/test/get_flash_sale",



    method:"POST",



     dataType: 'json',



    data:{book_id:rand_book,_token:_token},



    success:function(result)



    {



    //  $('#flash_title').text('')



    //  $('#flash_author').text('')



    //   $('#flash_img').attr('src',result.book_img);



    



    



    }







   });



    



    



    



   $("#flash_sale").removeClass('slide-out-left d-none').addClass('slide-in-left d-block');



}







function alertFunc2() {



    



     var book_list=$('#top_selling_book_ids').val();



           



           var books=book_list.split(',');



  var rand_book= get_random(books);







 var _token = $('input[name="_token"]').val();



    $.ajax({



    url:"/test/get_flash_sale",



    method:"POST",



     dataType: 'json',



    data:{book_id:rand_book,_token:_token},



    success:function(result)



    {



     $('#flash_title').text(result.title)



     $('#flash_author').text(result.author)



      $('#flash_img').attr('src',result.book_img);



    



    



    }







   });



    



        $("#flash_sale").removeClass('slide-in-left d-block').addClass('slide-out-left d-none');



}







  



  get_random = function (list) {



  return list[Math.floor((Math.random()*list.length))];



} 





     







    $(document).ready(function(){



        



      



      var buy_type= $('#buy_type').val(); 



      



      if(buy_type=='buy_book'){



          



           $('#tab1').css('display','block');



           $('#tab2').css('display','none');



           $('#tab3').css('display','none');



          



      }else if(buy_type=='rent_book'){



           $('#tab1').css('display','none');



           $('#tab2').css('display','block');



           $('#tab3').css('display','none');



          



      }else if(buy_type=='buy_chapter'){



          



           $('#tab1').css('display','none');



           $('#tab2').css('display','none');



           $('#tab3').css('display','block');



          



      }



      



     // alert(buy_type);



    });





     



    // function check_cat_main(cat_id){



       



    //     var className = $('#left_side_cat_main_'+cat_id).attr('class');



        



    //     $('#left_side_cat_main_'+cat_id).toggleClass("cat_active");



    // }



    



    //  function check_cat(cat_id){



       



    //     var className = $('#left_side_cat_main_'+cat_id).attr('class');



        



    //     $('#left_side_cat_'+cat_id).toggleClass("cat_active");



    // }





     



//     $(document).ready(function(){



       



//         toastr.success('The <strong>User</strong> record has been successfully updated.', 'Record Updated.');



        



//     });



// 

   


     



         $(function() {



            var availableTutorials  =  [



               "ActionScript",



               "Bootstrap",



               "C",



               "C++",



            ];



            $( "#search_input" ).autocomplete({



               source: availableTutorials



            });



         });



      

   
       



 $(document).ready(function(){  



      $('#search_input').keyup(function(){  



           var query = $(this).val();  



           //alert('ok');



           if(query != '')  



           {              



                $.ajax({  



                     method: 'POST',



                     url: 'https://www.ebookselibrary.com/get_autocomplete',



                     data: {"_token": "5Nal4ESjYMlHgXA3iFHsUYfFa6AbpNuNSU7RURFT", "value": query},  



                     success:function(data)  



                     {  



                        //console.log(data);



                          $('#countryList').removeClass('d-none');  



                          $('#countryList').fadeIn();  



                          $('#countryList').html(data);  



                     }  



                });  



           }  else {



            $('#countryList').fadeOut();



           }



      });  



      



        //   $('#search_input').onchange(function(){  



         



        //     $('#countryList').css('display','none');



           



        //   });



      



      



      $(document).on('click', '.storeClass', function(){  



           $('#search_input').val($(this).text());  



           $('#countryList').fadeOut();  



            $('#search_from').submit();  



      }); 



      



      



  var divToHide = document.getElementById('countryList');



  document.onclick = function(e){



    if(e.target.id !== 'countryList'){



      //element clicked wasn't the div; hide the div



      divToHide.style.display = 'none';



    }



  };



      



 });  



 



//  window.onload = function(){



//   var divToHide = document.getElementById('countryList');



//   document.onclick = function(e){



//     if(e.target.id !== 'countryList'){



//       //element clicked wasn't the div; hide the div



//       divToHide.style.display = 'none';



//     }



//   };



// };



 

     



    



    google.load("elements", "1", {



        packages: "transliteration"



    });







    function onLoadsearch() {



        var options = {



            sourceLanguage: google.elements.transliteration.LanguageCode.ENGLISH,



            destinationLanguage: [google.elements.transliteration.LanguageCode.HINDI],



            shortcutKey: 'ctrl+g',



            transliterationEnabled: false



        };







       



        var arr = [];



            



            arr.push('search_input');



            



        var control =



            new google.elements.transliteration.TransliterationControl(options);







       



        control.makeTransliteratable(arr);



    }



    



        //onLoad();



        google.setOnLoadCallback(onLoadsearch);



    



   

     



$(document).ready(function () {



    //Disable cut copy paste



    $('body').bind('cut copy paste', function (e) {



        e.preventDefault();



    });



    //Disable mouse right click



    $("body").on("contextmenu",function(e){



        return false;



    });



});





     



document.onkeydown = function(e) {



        if (e.ctrlKey && 



            (e.keyCode === 67 || 



             e.keyCode === 86 || 



             e.keyCode === 85 || 



             e.keyCode === 117)) {



            return false;



        } else {



            return true;



        }



};



$(document).keypress("u",function(e) {



  if(e.ctrlKey)



  {



return false;



}



else



{



return true;



}



});









     



    $(document).ready(function () {



      //createCaptcha();  



    });



var code;



function createCaptcha() {



  //clear the contents of captcha div first 



  document.getElementById('captcha').innerHTML = "";



  var charsArray =



  "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@!#$%^&*";



  var lengthOtp = 6;



  var captcha = [];



  for (var i = 0; i < lengthOtp; i++) {



    //below code will not allow Repetition of Characters



    var index = Math.floor(Math.random() * charsArray.length + 1); //get the next character from the array



    if (captcha.indexOf(charsArray[index]) == -1)



      captcha.push(charsArray[index]);



    else i--;



  }



  var canv = document.createElement("canvas");



  canv.id = "captcha";



  canv.width = 100;



  canv.height = 50;



  var ctx = canv.getContext("2d");



  ctx.font = "25px Georgia";



  ctx.strokeText(captcha.join(""), 0, 30);



  //storing captcha so that can validate you can save it somewhere else according to your specific requirements



  code = captcha.join("");



  document.getElementById("captcha").appendChild(canv); // adds the canvas to the body element



}



function validateCaptcha() {



  if (document.getElementById("cpatchaTextBox").value == code) {



    return true;



  }else{



createCaptcha();    



return false;



    



  }



}









    