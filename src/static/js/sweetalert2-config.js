/**
 * SweetAlert2 - Configuration simplifiée pour les messages Flash
 */

// Configuration de base pour les toasts
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 4000,
    timerProgressBar: true,
});

// Fonction pour afficher un toast d'erreur
function showErrorToast(message) {
    Toast.fire({
        icon: 'error',
        title: message,
    });
}

// Fonction pour afficher un toast de succès
function showSuccessToast(message) {
    Toast.fire({
        icon: 'success',
        title: message,
    });
}

// Fonction pour afficher les messages Flash de Flask
function showFlaskMessages() {
    const messages = JSON.parse(document.getElementById('flask-messages').textContent);

    messages.forEach(([category, message]) => {
        if (category.includes('error')) {
            showErrorToast(message);
        } else {
            showSuccessToast(message);
        }
    });
}

// Initialiser lorsque la page est chargée
document.addEventListener('DOMContentLoaded', () => {
    showFlaskMessages();
});