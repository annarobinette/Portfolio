window.addEventListener('scroll', function() {
    var header = document.querySelector('header');
    var scrollPosition = window.scrollY;

    if (scrollPosition > 100) { // Adjust this value as needed
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});