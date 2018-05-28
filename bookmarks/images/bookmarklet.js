//The below code is used for loading the JQuery from Googles CDN websites
//The number of attempts is limited to 15
(function(){
	var jquery_version = '2.1.4';
    var site_url = 'http://127.0.0.1:8000/';
    //static_url is the base URL for the static files available
    var static_url = site_url + 'static/';
    //The below min variables points for images that our bookmarkle code encounters
    var min_width = 100;
    var min_height = 100;
    function bookmarklet(msg) {
          // Here goes our bookmarklet code
		  // load CSS with a random number to avoid browser cache
		 var css = jQuery('<link>');
		css.attr({
			rel: 'stylesheet',
			type: 'text/css',
			href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
		});
		jQuery('head').append(css);
		// load HTML content and append to JQuery element
		box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
		jQuery('body').append(box_html);
		// close event
		//Removing the HTML element bookmarklet on click of close
		jQuery('#bookmarklet #close').click(function(){
		       jQuery('#bookmarklet').remove();
		});
		
		// find images and display them
		/* The selector img[src$="jpg"]   finds all the <img> HTML elements ,
		    for each element find image  URL and store in image_url and append it to JQuery */
		jQuery.each(jQuery('img[src$="jpg"]'), function(index, image) {
			if (jQuery(image).width() >= min_width && jQuery(image).height() >=min_height)
			{
				image_url = jQuery(image).attr('src');
				jQuery('#bookmarklet .images').append('<a href="#"><img src="'+image_url +'" /></a>');
			}
			});
			
			
		// when an image is selected open URL with it
		jQuery('#bookmarklet .images a').click(function(e){
				//This holds the URL of the selected image
				selected_image = jQuery(this).children('img').attr('src');
				// hide bookmarklet (id is given)
				jQuery('#bookmarklet').hide();
				// open new window to submit the image using window.open method of javascript
				window.open(site_url +'images/create/?url='
				+ encodeURIComponent(selected_image)
				+ '&title='
				+ encodeURIComponent(jQuery('title').text()),
				'_blank');
			});
    };
    // Check if jQuery is loaded
		if(typeof window.jQuery != 'undefined') {
				bookmarklet();
			}
		else
		{
			// Check for conflicts
			var conflict = typeof window.$ != 'undefined';
			// Create the script and point to Google API
			var script = document.createElement('script');
			script.setAttribute('src',
                            'http://ajax.googleapis.com/ajax/libs/jquery/' +
                            jquery_version + '/jquery.min.js');
			// Add the script to the 'head' for processing
			document.getElementsByTagName('head')[0].appendChild(script);
			// Create a way to wait until script loading
			var attempts = 15;
			(function(){
				// Check again if jQuery is undefined
				if(typeof window.jQuery == 'undefined') {
						if(--attempts > 0) {
						// Calls himself in a few milliseconds
						window.setTimeout(arguments.callee, 250)
				        }
						else {
							// Too much attempts to load, send error
							alert('An error ocurred while loading jQuery')
						}
				}
				else {
						bookmarklet();
				}
			})();
		}
})();
