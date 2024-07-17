document.addEventListener('DOMContentLoaded', function() {
    const errorIcons = document.querySelectorAll('.error-icon');

    errorIcons.forEach(icon => {
        const tooltip = icon.querySelector('.tooltip');
        icon.addEventListener('mouseenter', () => {
            tooltip.style.display = 'block';
        });
        icon.addEventListener('mouseleave', () => {
            tooltip.style.display = 'none';
        });
        icon.addEventListener('click', () => {
            tooltip.style.display = 'block';
        });
        icon.addEventListener('touchstart', () => {
            tooltip.style.display = 'block';
        });
        icon.addEventListener('touchend', () => {
            tooltip.style.display = 'block';
        });
    });
});