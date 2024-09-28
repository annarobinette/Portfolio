document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const normalScheme = document.getElementById('normal-scheme');
    const highContrastLight = document.getElementById('high-contrast-light');
    const highContrastDark = document.getElementById('high-contrast-dark');
    const textSmall = document.getElementById('text-small');
    const textNormal = document.getElementById('text-normal');
    const textLarge = document.getElementById('text-large');

    normalScheme.addEventListener('click', function() {
        body.className = '';
    });

    highContrastLight.addEventListener('click', function() {
        body.className = 'high-contrast-light';
    });

    highContrastDark.addEventListener('click', function() {
        body.className = 'high-contrast-dark';
    });

    textSmall.addEventListener('click', function() {
        body.classList.remove('text-large');
        body.classList.add('text-small');
    });

    textNormal.addEventListener('click', function() {
        body.classList.remove('text-small', 'text-large');
    });

    textLarge.addEventListener('click', function() {
        body.classList.remove('text-small');
        body.classList.add('text-large');
    });
});