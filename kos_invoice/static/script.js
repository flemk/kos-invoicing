function confirmAndRedirect(button, message) {
    event.preventDefault();
    if (confirm(message)) {
        var href = button.getAttribute('href');
        window.location.href = href;
    }
}