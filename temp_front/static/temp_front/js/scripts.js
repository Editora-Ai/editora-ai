/* Template: Tivo - SaaS App HTML Landing Page Template
   Author: Inovatik
   Created: Sep 2019
   Description: Custom JS file
*/

// Local var site_key = "6LeebLIZAAAAABaSN6j959jEqKBrp33xds0chbBo";
var site_key = $("#site_key_js").val();

(function($) {
    "use strict";

	/* Preloader */
	$(window).on('load', function() {
		var preloaderFadeOutTime = 500;
		function hidePreloader() {
			var preloader = $('.spinner-wrapper');
			setTimeout(function() {
				preloader.fadeOut(preloaderFadeOutTime);
			}, 500);
		}
		hidePreloader();
	});


	/* Navbar Scripts */
	// jQuery to collapse the navbar on scroll
    $(window).on('scroll load', function() {
		if ($(".navbar").offset().top > 60) {
			$(".fixed-top").addClass("top-nav-collapse");
		} else {
			$(".fixed-top").removeClass("top-nav-collapse");
		}
    });

	// jQuery for page scrolling feature - requires jQuery Easing plugin
	$(function() {
		$(document).on('click', 'a.page-scroll', function(event) {
			var $anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $($anchor.attr('href')).offset().top
			}, 600, 'easeInOutExpo');
			event.preventDefault();
		});
	});

    // closes the responsive menu on menu item click
    $(".navbar-nav li a").on("click", function(event) {
    if (!$(this).parent().hasClass('dropdown'))
        $(".navbar-collapse").collapse('hide');
    });


    /* Image Slider - Swiper */
    var imageSlider = new Swiper('.image-slider', {
        autoplay: {
            delay: 2000,
            disableOnInteraction: false
		},
        loop: true,
        spaceBetween: 30,
        slidesPerView: 5,
		breakpoints: {
            // when window is <= 580px
            580: {
                slidesPerView: 1,
                spaceBetween: 10
            },
            // when window is <= 768px
            768: {
                slidesPerView: 2,
                spaceBetween: 20
            },
            // when window is <= 992px
            992: {
                slidesPerView: 3,
                spaceBetween: 20
            },
            // when window is <= 1200px
            1200: {
                slidesPerView: 4,
                spaceBetween: 20
            },

        }
    });


    /* Text Slider - Swiper */
	var textSlider = new Swiper('.text-slider', {
        autoplay: {
            delay: 6000,
            disableOnInteraction: false
		},
        loop: true,
        navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev'
		}
    });


    /* Video Lightbox - Magnific Popup */
    $('.popup-youtube, .popup-vimeo').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false,
        iframe: {
            patterns: {
                youtube: {
                    index: 'youtube.com/',
                    id: function(url) {
                        var m = url.match(/[\\?\\&]v=([^\\?\\&]+)/);
                        if ( !m || !m[1] ) return null;
                        return m[1];
                    },
                    src: 'https://www.youtube.com/embed/%id%?autoplay=1'
                },
                vimeo: {
                    index: 'vimeo.com/',
                    id: function(url) {
                        var m = url.match(/(https?:\/\/)?(www.)?(player.)?vimeo.com\/([a-z]*\/)*([0-9]{6,11})[?]?.*/);
                        if ( !m || !m[5] ) return null;
                        return m[5];
                    },
                    src: 'https://player.vimeo.com/video/%id%?autoplay=1'
                }
            }
        }
    });


    /* Details Lightbox - Magnific Popup */
	$('.popup-with-move-anim').magnificPopup({
		type: 'inline',
		fixedContentPos: false, /* keep it false to avoid html tag shift with margin-right: 17px */
		fixedBgPos: true,
		overflowY: 'auto',
		closeBtnInside: true,
		preloader: false,
		midClick: true,
		removalDelay: 300,
		mainClass: 'my-mfp-slide-bottom'
	});


    /* Move Form Fields Label When User Types */
    // for input and textarea fields
    $("input, textarea").keyup(function(){
		if ($(this).val() != '') {
			$(this).addClass('notEmpty');
		} else {
			$(this).removeClass('notEmpty');
		}
    });

    /* Sign Up Form */
    grecaptcha.ready(function() {

        $("#signUpForm").validator().on("submit", function(event) {
            if (event.isDefaultPrevented()) {
                // handle the invalid form...
                sformError();
                ssubmiterrorMSG(false, "Please fill all fields!");
            } else {
                // everything looks good!
                event.preventDefault();
                grecaptcha.execute(site_key, {action: 'logInForm'}).then(function(token) {
                    var g_token = token
                    ssubmitForm(g_token);
            });
            }
        });
    });

    function ssubmitForm(g_token) {
        // initiate variables with form content
		var email = $("#semail").val();
        var name = $("#fname").val();
        var lastname = $("#lname").val();
        var password = $("#spassword").val();
        var company = $("#company").val();
        var msgClasses = "h3 text-center";

        $("#smsgSubmit").removeClass().addClass(msgClasses).text("Please wait...!");
        $.ajax({
            type: "POST",
            url: "sign-up",
            data: "email=" + email + "&company=" + company + "&firstname=" + name + "&password1=" + password + "&password2=" + password + "&lastname=" + lastname + "&token=" + g_token,
            success: function(text) {
                sformSuccess("Successfully Registered. Please check your email to activate your account!");
            },
            error: function(text) {
                validmailorpass(text.responseText)
            }
        });
    }
    function validmailorpass(text) {
        var msgClasses = "h3 text-center";
        var myerror = JSON.parse(text);
        try {
            var message = myerror.email[0];
        } catch (e) {
            var message = "Password must contain at least 8 characters and not entirely numeric!"
        }
        $("#smsgSubmit").removeClass().addClass(msgClasses).text(message);
    }

    function sformSuccess(message) {
        var msgClasses = "h3 text-center";
        $("#smsgSubmit").removeClass().addClass(msgClasses).text(message);
    }

    function sformError() {
        $("#signUpForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}
    function ssubmiterrorMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#smsgSubmit").removeClass().addClass(msgClasses).text("Fill required forms first!");
    }

    function ssubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#smsgSubmit").removeClass().addClass(msgClasses).text("You have successfully registered!");
        setTimeout(function(){ window.location = "dashboard/"; }, 500);
    }

    /* Log In Form */
    grecaptcha.ready(function() {

        $("#logInForm").validator().on("submit", function(event) {
            if (event.isDefaultPrevented()) {
                // handle the invalid form...
                lformError();
                lsubmiterrorMSG(false, "Please fill all fields!");
            } else {
                // everything looks good!
                event.preventDefault();
                grecaptcha.execute(site_key, {action: 'logInForm'}).then(function(token) {
                    var g_token = token
                    lsubmitForm(g_token);
                });
            }
        });
    });

    function lsubmitForm(g_token) {
        // initiate variables with form content
		var email = $("#lemail").val();
		var password = $("#lpassword").val();
        var msgClasses = "h3 text-center";

        $.ajax({
            type: "POST",
            url: "log-in",
            data: "email=" + email + "&password=" + password + "&token=" + g_token,
            success: function(text) {
                lsubmitMSG(text);
            },
            error: function(text) {
                lsubmiterrorMSG(text);
            }
        });
	}

    function lformSuccess() {
        $("#logInForm")[0].reset();
        lsubmitMSG(true, "Log In Submitted!");
        $("input").removeClass('notEmpty'); // resets the field label after submission
    }

    function lformError() {
        $("#logInForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}

    function lsubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#lmsgSubmit").removeClass().addClass(msgClasses).text("Log In Submitted!");
        setTimeout(function(){ window.location = "dashboard/"; }, 500);
    }

    function lsubmiterrorMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#lmsgSubmit").removeClass().addClass(msgClasses).text("Email or Password is incorrect!");
    }


    /* Reset Password Form */
    $("#resetpassForm").validator().on("submit", function(event) {
        if (event.isDefaultPrevented()) {
            // handle the invalid form...
            resetpassformError();
            resetpasssubmiterrorMSG(false, "Please fill the email field!");
        } else {
            // everything looks good!
            event.preventDefault();
            resetpasssubmitForm();
        }
    });

    function resetpasssubmitForm() {
        // initiate variables with form content
        var email = $("#resetemail").val();
        var msgClasses = "h6 text-center tada animated";

        $("#resetpassmsgSubmit").removeClass().addClass(msgClasses).text("Please wait...!");
        $.ajax({
            type: "POST",
            url: "rest-auth/password/reset/",
            data: "email=" + email,
            success: function(text) {
                resetpasssubmitMSG(text);
            },
            error: function(text) {
                resetpasssubmiterrorMSG(text);
            }
        });
    }

    function resetpassformError() {
        $("resetpassForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
    }

    function resetpasssubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h6 text-center tada animated";
        } else {
            var msgClasses = "h6 text-center";
        }
        $("#resetpassmsgSubmit").removeClass().addClass(msgClasses).text("A link has been sent to your email!");
    }

    function resetpasssubmiterrorMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h6 text-center tada animated";
        } else {
            var msgClasses = "h6 text-center";
        }
        $("#resetpassmsgSubmit").removeClass().addClass(msgClasses).text("Email is not correct!");
    }


    /* Reset Password Confirm Form */
    $("#resetpasswordconfirmForm").validator().on("submit", function(event) {
        if (event.isDefaultPrevented()) {
            // handle the invalid form...
            resetpasswordconfirmError();
            resetpasswordconfirmsubmiterrorMSG(false, "Please fill the email field!");
        } else {
            // everything looks good!
            event.preventDefault();
            resetpasswordconfirmsubmitForm();
        }
    });

    function resetpasswordconfirmsubmitForm() {
        // initiate variables with form content
        var password = $("#resetpasswordconfirm").val();
        var uuid = location.pathname.split("/")[5]
        var token = location.pathname.split("/")[6]

        $.ajax({
            type: "POST",
            url: "/rest-auth/password/reset/confirm/",
            data: "new_password1=" + password + "&new_password2=" + password + "&uid=" + uuid + "&token=" + token,
            success: function(text) {
                resetpasswordconfirmsubmitMSG(text);
            },
            error: function(text) {
                resetpasswordconfirmsubmiterrorMSG(text);
            }
        });
    }

    function resetpasswordconfirmsubmiterrorMSG() {
        $("resetpassForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
    }

    function resetpasswordconfirmsubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h6 text-center tada animated";
        } else {
            var msgClasses = "h6 text-center";
        }
        $("#resetpasswordconfirmmsgSubmit").removeClass().addClass(msgClasses).text("Your password is updated!");
        setTimeout(function(){ window.location = "/log-in"; }, 500);

    }

    function resetpasswordconfirmsubmiterrorMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h6 text-center tada animated";
        } else {
            var msgClasses = "h6 text-center";
        }
        $("#resetpasswordconfirmmsgSubmit").removeClass().addClass(msgClasses).text("Password must contain at least 8 characters and not entirely numeric! also don't try your old password.");
    }

    /* Back To Top Button */
    // create the back to top button
    $('body').prepend('<a href="body" class="back-to-top page-scroll">Back to Top</a>');
    var amountScrolled = 700;
    $(window).scroll(function() {
        if ($(window).scrollTop() > amountScrolled) {
            $('a.back-to-top').fadeIn('500');
        } else {
            $('a.back-to-top').fadeOut('500');
        }
    });


	/* Removes Long Focus On Buttons */
	$(".button, a, button").mouseup(function() {
		$(this).blur();
	});

})(jQuery);