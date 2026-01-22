/**
 * SweetAlert2 - Configuration ultra-simple
 * Juste ce qu'il faut pour que ça marche bien
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

// Fonction pour afficher un toast et le stocker dans sessionStorage
function showPersistentToast(type, message) {
    // Stocker dans sessionStorage
    let toasts = JSON.parse(sessionStorage.getItem('persistentToasts') || '[]');
    toasts.push({type, message, timestamp: Date.now()});
    sessionStorage.setItem('persistentToasts', JSON.stringify(toasts));
    
    // Afficher immédiatement
    if (type === 'error') {
        showErrorToast(message);
    } else {
        showSuccessToast(message);
    }
}

// Fonction pour afficher les toasts persistants au chargement de la page
function showPersistentToasts() {
    const toasts = JSON.parse(sessionStorage.getItem('persistentToasts') || '[]');
    const now = Date.now();
    
    // Filtrer les toasts récents (moins de 5 minutes)
    const recentToasts = toasts.filter(toast => now - toast.timestamp < 300000);
    
    if (recentToasts.length > 0) {
        recentToasts.forEach(toast => {
            if (toast.type === 'error') {
                showErrorToast(toast.message);
            } else {
                showSuccessToast(toast.message);
            }
        });
    }
    
    // Nettoyer le storage après affichage
    sessionStorage.removeItem('persistentToasts');
}

// Initialiser lorsque la page est chargée
document.addEventListener('DOMContentLoaded', () => {
    showFlaskMessages();
    showPersistentToasts();
});