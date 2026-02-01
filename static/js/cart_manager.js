document.addEventListener('DOMContentLoaded', function() {
    // Toastr Configuration
    if (typeof toastr !== 'undefined') {
        toastr.options = {
            "closeButton": true,
            "debug": false,
            "newestOnTop": true,
            "progressBar": true,
            "positionClass": "toast-top-right",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "3000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        };
    }

    // Helper to show toast
    window.showToast = function(message, tag) {
        if (typeof toastr === 'undefined') {
            console.log(tag + ": " + message);
            return;
        }
        
        switch(tag) {
            case 'success':
                toastr.success(message);
                break;
            case 'info':
                toastr.info(message);
                break;
            case 'warning':
                toastr.warning(message);
                break;
            case 'error':
                toastr.error(message);
                break;
            default:
                toastr.info(message);
        }
    };

    // CSRF Token Helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Handle Add to Cart and Increment/Decrement
    document.body.addEventListener('click', function(e) {
        const btn = e.target.closest('.update-cart') || e.target.closest('.add-to-cart-btn');
        
        if (btn) {
            const productId = btn.dataset.id;
            if (!productId) return;

            e.preventDefault();
            let quantity = 1;
            
            if (btn.dataset.action === 'decrease') {
                quantity = -1;
            }
            
            updateCart(productId, quantity);
        }
    });

    function updateCart(productId, quantity) {
        // --- Optimistic UI Update Start ---
        const elementsToUpdate = [
            { group: `qty-group-${productId}`, btn: `add-btn-${productId}`, input: `qty-input-${productId}` },
            { group: `qty-group-modal-${productId}`, btn: `add-btn-modal-${productId}`, input: `qty-input-modal-${productId}` }
        ];

        // 1. Update Item Quantity UI immediately
        elementsToUpdate.forEach(ids => {
            const qtyGroup = document.getElementById(ids.group);
            const addBtn = document.getElementById(ids.btn);
            const qtyInput = document.getElementById(ids.input);

            if (qtyInput) {
                let currentVal = parseInt(qtyInput.value) || 0;
                let newVal = currentVal + quantity;
                
                if (newVal <= 0) {
                    newVal = 0;
                    if (qtyGroup) qtyGroup.classList.add('d-none');
                    if (addBtn) addBtn.classList.remove('d-none');
                } else {
                    if (qtyGroup) qtyGroup.classList.remove('d-none');
                    if (addBtn) addBtn.classList.add('d-none');
                }
                qtyInput.value = newVal;
            }
        });

        // 2. Update Global Cart Count UI immediately
        const navCartCount = document.getElementById('cart-count');
        if (navCartCount) {
            let currentCount = parseInt(navCartCount.textContent) || 0;
            let newCount = Math.max(0, currentCount + quantity);
            navCartCount.textContent = newCount;
            if (newCount > 0) {
                navCartCount.classList.remove('d-none');
            } else {
                navCartCount.classList.add('d-none');
            }
        }
        // --- Optimistic UI Update End ---

        fetch(`/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `quantity=${quantity}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Show notification
                showToast(data.message, data.message_tag);

                // Reconcile with server data (Source of Truth)
                elementsToUpdate.forEach(ids => {
                    const qtyGroup = document.getElementById(ids.group);
                    const addBtn = document.getElementById(ids.btn);
                    const qtyInput = document.getElementById(ids.input);
                
                // Update cart count in navbar
                if (navCartCount) {
                    navCartCount.textContent = data.cart_count;
                    if (data.cart_count > 0) {
                        navCartCount.classList.remove('d-none');
                    } else {
                        navCartCount.classList.add('d-none');
                    }
                }

                // Toggle buttons
                if (data.item_quantity > 0) {
                    if (qtyGroup) qtyGroup.classList.remove('d-none');
                    if (addBtn) addBtn.classList.add('d-none');
                    if (qtyInput) qtyInput.value = data.item_quantity;
                } else {
                    if (qtyGroup) qtyGroup.classList.add('d-none');
                    if (addBtn) addBtn.classList.remove('d-none');
                    if (qtyInput) qtyInput.value = 0;
                }
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }
});