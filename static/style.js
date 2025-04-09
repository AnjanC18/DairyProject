// Global variables
let milkPrices = {};

// Document Ready Function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();
    
    // Initialize form validations
    initFormValidations();
    
    // Load milk prices if available
    if (document.getElementById('milk_type')) {
        loadMilkPrices();
    }
    
    // Initialize animations
    initAnimations();
});

// Initialize Tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const tooltipText = this.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    
    document.body.appendChild(tooltip);
    
    const rect = this.getBoundingClientRect();
    tooltip.style.left = `${rect.left + rect.width/2 - tooltip.offsetWidth/2}px`;
    tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
    
    this.tooltip = tooltip;
}

function hideTooltip() {
    if (this.tooltip) {
        this.tooltip.remove();
    }
}

// Form Validations
function initFormValidations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = 'var(--berry-red)';
                    isValid = false;
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill in all required fields', 'danger');
            }
        });
    });
}

// Milk Price Calculations
function loadMilkPrices() {
    // This would typically come from an API or server-side rendering
    const milkTypeSelect = document.getElementById('milk_type');
    const priceElements = document.querySelectorAll('[data-milk-price]');
    
    if (priceElements.length > 0) {
        priceElements.forEach(element => {
            const milkType = element.getAttribute('data-milk-type');
            const price = element.getAttribute('data-milk-price');
            milkPrices[milkType] = parseFloat(price);
        });
    }
    
    if (milkTypeSelect) {
        milkTypeSelect.addEventListener('change', updateTotalPrice);
        document.getElementById('quantity').addEventListener('input', updateTotalPrice);
    }
}

function updateTotalPrice() {
    const milkType = document.getElementById('milk_type').value;
    const quantity = parseFloat(document.getElementById('quantity').value) || 0;
    const pricePerLiter = milkPrices[milkType] || 0;
    const totalPrice = quantity * pricePerLiter;
    
    document.getElementById('total_price').value = totalPrice.toFixed(2);
}

// Animations
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate');
    
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = `fadeIn 0.5s forwards`;
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(element);
    });
}

// Alert System
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 500);
    }, 5000);
}

// Edit Functionality for Milk Details
function enableEdit(rowId) {
    const priceInput = document.getElementById(`price-${rowId}`);
    const saveButton = document.getElementById(`save-${rowId}`);
    const editButton = document.getElementById(`edit-${rowId}`);
    
    priceInput.disabled = false;
    priceInput.focus();
    saveButton.style.display = "inline-block";
    editButton.style.display = "none";
    
    // Add animation
    priceInput.style.animation = 'pulse 0.5s';
    setTimeout(() => {
        priceInput.style.animation = '';
    }, 500);
}

function validateEdit(rowId) {
    const priceInput = document.getElementById(`price-${rowId}`);
    
    if (priceInput.disabled) {
        showAlert("Click on Edit first to change the price.", "danger");
        return false;
    }
    
    if (parseFloat(priceInput.value) <= 0) {
        showAlert("Price must be greater than 0", "danger");
        return false;
    }
    
    return true;
}

// Utility Functions
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}