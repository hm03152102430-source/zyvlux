// js Document

    // Created on   : 20/09/2023.
    // Theme Name   : khuj -the job finder creative bootstrap 5 template
    // Version      : 1.0.
    // Developed by : (sayfurrahaman265@gmail.com) / (www.me.heloshape.com)


(function($) {
    "use strict";
// ===============theam switcher
   
 // ----------------------------- Counter Function
        var timer = $('.counter');
        if(timer.length) {
          $('.counter').counterUp({
            delay: 10,
            time: 1200,
          });
        }
    // ------------------------ Navigation Scroll

        $(window).on('scroll', function (){   
          var sticky = $('.sticky-menu'),
          scroll = $(window).scrollTop();
          if (scroll >= 100) sticky.addClass('fixed');
          else sticky.removeClass('fixed');

        });
// -------------------- From Bottom to Top Button

        $(window).on('scroll', function (){
          if ($(this).scrollTop() > 200) {
            $('.scroll-top').fadeIn();
          } else {
            $('.scroll-top').fadeOut();
          }
        });
//---------------------- Click event to scroll to top

        $('.scroll-top').on('click', function() {
          $('html, body').animate({scrollTop : 0});
          return false;
        });

//-------------------------- banner one slider

          if($("#banner_slider_one").length) {
            $('#banner_slider_one').slick({
              dots: false,
              arrows: false,
              autoplaySpeed: 3000,
              speed: 500,
              cssEase: "linear",
              pauseOnHover: true,
              autoplay: true,
              touchMove: true,
              useCSS: true,
              useTransform: true,
              });
          };
          //-------------------------- banner one slider

          if($(".banner_two_slider").length) {
            $('.banner_two_slider').slick({
              dots: false,
              arrows: false,
              slidesToShow: 1,
              slidesToScroll: 1,
              speed: 600,
              autoplaySpeed: 2000,
              autoplay: true,
              });
          };
    // partner slider
    if($("#testimonial_slider_one").length) {
          $('#testimonial_slider_one').slick({
              dots: true,
              arrows: true,
              prevArrow:'<span class="slick-previous"><i class="bi bi-arrow-left"></i></span>',
              nextArrow:'<span class="slick-next"><i class="bi bi-arrow-right"></i></span>',
              slidesToShow:1,
              slidesToScroll:1,
              infinite: true,
              lazyLoad: 'ondemand',
              autoplay: true,
              autoplaySpeed:3000,
            });
        };
 // partner slider-two
    if($("#partner_slider").length) {
          $('#partner_slider').slick({
              dots: false,
              arrows: false,
              slidesToShow:5,
              slidesToScroll:1,
              infinite: true,
              lazyLoad: 'ondemand',
              autoplay: true,
              autoplaySpeed:3000,
              responsive: [
                {
                  breakpoint:1200,
                  settings: {
                    slidesToShow: 4,
                    slidesToScroll:1
                  }
                },
                {
                  breakpoint:992,
                  settings: {
                    slidesToShow:3,
                    slidesToScroll:1
                  }
                },
                {
                  breakpoint: 768,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll:1
                  }
                },
                {
                  breakpoint: 576,
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll:1
                  }
                }
              ]
            });
        };
// ------------------------ Feedback Slider One

        if($(" #testimonial_slider").length) {
          $(' #testimonial_slider').slick({
              dots: false,
              prevArrow:'<i class="bi bi-chevron-left"></i>',
              nextArrow:'<i class="bi bi-chevron-right"></i>',
              centerPadding: '0px',
              slidesToShow: 3,
              slidesToScroll:3,
              autoplay: true,
              centerMode: true,
              autoplaySpeed: 3000,
              responsive: [
                {
                  breakpoint:1199.98,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll:3
                  }
                },
                {
                  breakpoint:991.98,
                  settings: {
                    slidesToShow:2,
                    slidesToScroll:3
                  }
                },
                {
                  breakpoint:767.98,
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll:3
                  }
                },
                {
                  breakpoint: 575,
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll:3
                  }
                }
              ]
            });
        };
// ------------------------ Feedback Slider two

        if($("#testimonial-slider-two").length) {
          $('#testimonial-slider-two').slick({
            dots: true,
            arrows: true,
            prevArrow:'<span class="slick-previous"><i class="bi bi-arrow-left"></i></span>',
            nextArrow:'<span class="slick-next"><i class="bi bi-arrow-right"></i></span>',
            slidesToShow:1,
            slidesToScroll:1,
            infinite: true,
            lazyLoad: 'ondemand',
            autoplay: true,
            autoplaySpeed:3000
            });
        };

$(window).on ('load', function (){ 

  // -------------------- Site Preloader

        $('#andeo-preloader').fadeOut('fast'); // will first fade out the loading animation
        $('#preloader').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website.
        $('body').delay(350).css({'overflow':'visible'});


        if($(".view_pic").length) {
          $('.view_pic').magnificPopup({
            type: 'image',
            closeOnContentClick: true,
            closeBtnInside: false,
            fixedContentPos: true,
            mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
            image: {
              verticalFit: true
            },
            zoom: {
              enabled: true,
              duration: 500 // don't foget to change the duration also in CSS
            }
          });
         };

       // ----------------------------- isotop gallery
       if ($("#isotop-gallery-wrapper").length) {
        var $grid = $('#isotop-gallery-wrapper').isotope({
          // options
          itemSelector: '.isotop-item',
          layoutMode: 'fitRows',
          masonry: {
            // use element for option
            columnWidth: '.grid-sizer',
          }

        });

        // filter items on button click
        $('.isotop-menu-wrapper').on( 'click', 'li', function() {
          var filterValue = $(this).attr('data-filter');
          $grid.isotope({ filter: filterValue });
        });

        // change is-checked class on buttons
        $('.isotop-menu-wrapper').each( function( i, buttonGroup ) {
            var $buttonGroup = $( buttonGroup );
            $buttonGroup.on( 'click', 'li', function() {
              $buttonGroup.find('.is-checked').removeClass('is-checked');
              $( this ).addClass('is-checked');
            });
        });
       }
       //magnificPopup video

       if($(".watch-video").length){
        $('.watch-video').magnificPopup({
          disableOn: 700,
          type: 'iframe',
          mainClass: 'mfp-fade',
          removalDelay: 160,
          preloader: true,
          fixedContentPos: true
        });
      };
      // ------------------------------- wow Animation
      var wow = new WOW(
        {
          boxClass:     'wow',      // animated element css class (default is wow)
          animateClass: 'animated', // animation css class (default is animated)
          offset:       0,          // distance to the element when triggering the animation (default is 0)
          mobile:       true,       // trigger animations on mobile devices (default is true)
          live:         true       // act on asynchronously loaded content (default is true)
        }
      );
      wow.init();

    });  //End On Load Function

})(jQuery);