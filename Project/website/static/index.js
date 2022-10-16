var sIndex = 1;
showSlide(sIndex);

// Next/previous controls
function plusSlides(n) {
  showSlide(sIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlide(sIndex = n);
}

function showSlide(n) {
  var i;
  var slide = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slide.length) {sIndex = 1}
  if (n < 1) {sIndex = slide.length}
  for (i = 0; i < slide.length; i++) {
      slide[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slide[sIndex-1].style.display = "block";
  dots[sIndex-1].className += " active";
} 


var slideIndex = 0;
showSlides();

function showSlides() {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}
  slides[slideIndex-1].style.display = "block";
  setTimeout(showSlides, 2500); // Change image every 2.5 seconds
}


