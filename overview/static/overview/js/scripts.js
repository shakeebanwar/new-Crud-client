(function ($) {
    $(document).ready(function () {

        // Scroll to Top
        jQuery('.scrolltotop').click(function () {
            jQuery('html').animate({'scrollTop': '0px'}, 400);
            return false;
        });

        jQuery(window).scroll(function () {
            var upto = jQuery(window).scrollTop();
            if (upto > 500) {
                jQuery('.scrolltotop').fadeIn();
            } else {
                jQuery('.scrolltotop').fadeOut();
            }
        });

    });
})(jQuery);


// $('#office-booking-button').on('click', function (event) {
// 	event.preventDefault();
//     console.log("form submitted!")  // sanity check
//     $.ajax({
//         url: '',
//         type: 'get',
//         data: {
//             button_text: $(this).text()
//         },
//         success: function (response) {
//             $('#office-booking-button').text(response.seconds)
//         });
// });
// });


// function create_post() {
//     console.log("create post is working!") // sanity check
//     // console.log($('#post-text').val())
// };

// $(document).ready(function(){
//
// 	$('.office_button').click(function(){
// 		$.ajax({
// 			url: '',
// 			type: 'get',
// 			data: {
// 				button_text: $(this).text()
// 			},
// 			success: function(response) {
// 				$('.office_button').text(response.seconds)
// 			}
//
// 		});
//
// 	});
//
// });