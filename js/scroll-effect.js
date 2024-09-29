document.addEventListener('DOMContentLoaded', function() {
  const header = document.querySelector('header');
  const headerHeight = header.offsetHeight;
  const scrollThreshold = headerHeight / 2; // Start transition halfway through the header

  window.addEventListener('scroll', function() {
      const scrollPosition = window.scrollY;
      const scrollPercentage = Math.min(1, Math.max(0, (scrollPosition - scrollThreshold) / headerHeight));
      
      header.style.setProperty('--scroll-percentage', scrollPercentage);
      
      if (scrollPosition > 0) {
          header.classList.add('scrolling');
      } else {
          header.classList.remove('scrolling');
      }
      
      if (scrollPercentage >= 1) {
          header.classList.add('scrolled');
      } else {
          header.classList.remove('scrolled');
      }
  });
});