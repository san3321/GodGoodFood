		var xhr = new XMLHttpRequest();
		var url = "http://localhost:8000";
		var lat = "";
		var lon = "";
		var isRequestSending = false;
	  	var response = "";
	    var now = new Date().getTime();
  		var currentImageIndex = 9;
  		var repeatCounter = 0;

        $( "#icons" ).click(hideImage);

        $("#add-new-rest-action").click(function(){
          document.getElementById("search-section").style.visibility = "visible";
        });

        $("#send-new-rest").click(function(){
          document.getElementById("search-section").style.visibility = "hidden";
        });

		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(showPosition);
		} else { 
			x.innerHTML = "Geolocation is not supported by this browser.";
		}		
				
		function showPosition(position) {
				lat = position.coords.latitude
				lon = position.coords.longitude
			}
				
		function sendLocationRequest(){
			isRequestSending = true;
			xhr.open("POST", url, true);
			xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
			xhr.onreadystatechange = function () {
			if (xhr.readyState === 4 && xhr.status === 200) {
				var json = JSON.parse(xhr.responseText);
				console.log(json.name + " | " + json.address +" | " + json.lat + " | " + json.lon + " | Обед: " + json.lunch + " | Оплата картой: " + json.credit_card + " | Средний счёт: " + json.average_bill + " | Завтрак: " + json.breakfast); //Ответ от .py
				response = json.name + ", " + json.address;
				isRequestSending = false;
			}
		}

		if (lat) {
			var data = JSON.stringify({"lat": lat, "lon": lon});
			console.log(data)
			xhr.send(data);
		} else if (repeatCounter < 3) {
			repeatCounter++;
			sendLocationRequest()
		} else if (repeatCounter == 10) {
			isRequestSending = false;
			console.log("22");
			return;
		}
		}
	
	  $( function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 2000,
      values: [ 200, 1000 ],
      slide: function( event, ui ) {
        $( "#amount" ).val(ui.values[ 0 ]+ "р" + " - " + ui.values[ 1 ] + "р");
      }
    });
    $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) + "р" +
      " - " + $( "#slider-range" ).slider( "values", 1 ) + "р" );
  } );
	  
   $( "#place-to-eat" ).fadeOut(0);
  
  var arrayOfImages = document.getElementsByClassName("food-icon");
        
    function hideImage(){
	  if (!isRequestSending && response.length == 0){
	  	   sendLocationRequest()
	  };
		
      arrayOfImages[currentImageIndex].style.visibility = "hidden";
      if (currentImageIndex > 0) {
        currentImageIndex -= 1;
        if (currentImageIndex == 1 && isRequestSending) {
          makeAllImagesVisible()
          currentImageIndex = 9;
          setTimeout(hideImage, 75);
          return;
        } else {
          setTimeout(hideImage, 75);
        }    
		  
      } else {
        currentImageIndex = 9;
        makeAllImagesVisible();
        rotateAndFadeOut();
		isRequestSending = false;
      }
    }
    
    function makeAllImagesVisible() {
      Array.from(arrayOfImages).forEach(function(element) {
        element.style.visibility = "visible";
        });
    }
    
    function rotateAndFadeOut() {
      $( "#icons" ).fadeOut(1000);
     	document.getElementById("place-to-eat").style.visibility = "visible";
      $( "#place-to-eat" ).fadeIn(1500);
      arrayOfImages[currentImageIndex].style.boxShadow = "0px 0px 10px 40px rgba(230,245,255,0.3)";
      document.getElementById("icons").style.transform = "rotateY(180deg)";
	  document.getElementById("place-to-eat").textContent = response;
    } 