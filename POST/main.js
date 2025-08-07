// Store Management System
const store = {
    products: [],
    customers: [],
    sales: [],
    expenses: [],
    cashbox: {
        balance: 0,
        transactions: []
    },
    settings: {
        currency: 'ر.س',
        storeName: 'نظام المتجر',
        taxRate: 15,
        dateFormat: 'dd/mm/yyyy'
    }
};

// DOM Elements
const sections = {
    dashboard: document.getElementById('dashboard'),
    products: document.getElementById('products'),
    sales: document.getElementById('sales'),
    customers: document.getElementById('customers'),
    expenses: document.getElementById('expenses'),
    settings: document.getElementById('settings')
};

// Navigation Functions
function showSection(sectionId) {
    // Hide all sections
    Object.values(sections).forEach(section => {
        section.style.display = 'none';
    });

    // Show selected section
    if (sections[sectionId]) {
        sections[sectionId].style.display = 'block';
    }
}

// Data Management
function saveData() {
    localStorage.setItem('storeData', JSON.stringify(store));
}

function loadData() {
    const savedData = localStorage.getItem('storeData');
    if (savedData) {
        store.products = JSON.parse(savedData).products || [];
        store.customers = JSON.parse(savedData).customers || [];
        store.sales = JSON.parse(savedData).sales || [];
        store.expenses = JSON.parse(savedData).expenses || [];
        store.cashbox = JSON.parse(savedData).cashbox || {
            balance: 0,
            transactions: []
        };
        store.settings = JSON.parse(savedData).settings || {
            currency: 'ر.س',
            storeName: 'نظام المتجر',
            taxRate: 15,
            dateFormat: 'dd/mm/yyyy'
        };
    }
}

// Initialize the application
function initApp() {
    loadData();
    updateUI();
    document.querySelector('.loading').style.display = 'none';
}

// UI Management
function updateUI() {
    updateDashboard();
    updateProductsTable();
    updateCustomersTable();
    updateSalesTable();
    updateExpensesTable();
}

// Dashboard Functions
function updateDashboard() {
    // Calculate total sales
    const totalSales = store.sales.reduce((sum, sale) => sum + sale.total, 0);
    
    // Calculate total expenses
    const totalExpenses = store.expenses.reduce((sum, expense) => sum + expense.amount, 0);
    
    // Calculate net profit
    const netProfit = totalSales - totalExpenses;
    
    // Update dashboard with these values
    document.getElementById('totalSalesAmount').textContent = `${totalSales.toFixed(2)} ${store.settings.currency}`;
    document.getElementById('totalExpensesAmount').textContent = `${totalExpenses.toFixed(2)} ${store.settings.currency}`;
    document.getElementById('netProfitAmount').textContent = `${netProfit.toFixed(2)} ${store.settings.currency}`;
}

// Product Management
function addProduct(name, price, quantity, category) {
    const productId = Date.now().toString();
    const newProduct = {
        id: productId,
        name,
        price,
        quantity,
        category,
        createdAt: new Date().toISOString()
    };
    
    store.products.push(newProduct);
    saveData();
    return newProduct;
}

function updateProductQuantity(productId, newQuantity) {
    const product = store.products.find(p => p.id === productId);
    if (product) {
        product.quantity = newQuantity;
        saveData();
    }
}

function removeProduct(productId) {
    store.products = store.products.filter(p => p.id !== productId);
    saveData();
}

// Sales Functions
function startSale(customerId) {
    const customer = store.customers.find(c => c.id === customerId);
    const saleId = Date.now().toString();
    const newSale = {
        id: saleId,
        customerId: customerId || null,
        customerName: customer ? customer.name : '',
        items: [],
        total: 0,
        date: new Date().toISOString()
    };
    
    store.sales.push(newSale);
    saveData();
    return newSale;
}

function addItemToSale(saleId, productId, quantity) {
    const sale = store.sales.find(s => s.id === saleId);
    if (!sale) return false;
    
    const product = store.products.find(p => p.id === productId);
    if (!product) return false;
    
    // Check if product already exists in sale
    const existingItemIndex = sale.items.findIndex(item => item.productId === productId);
    if (existingItemIndex !== -1) {
        sale.items[existingItemIndex].quantity += quantity;
    } else {
        sale.items.push({
            productId,
            name: product.name,
            price: product.price,
            quantity,
            total: product.price * quantity
        });
    }
    
    // Update sale total
    sale.total = sale.items.reduce((sum, item) => sum + item.total, 0);
    
    saveData();
    return true;
}

function completeSale(saleId, paymentMethod, notes) {
    const sale = store.sales.find(s => s.id === saleId);
    if (!sale) return false;
    
    // Update cashbox
    store.cashbox.balance += sale.total;
    store.cashbox.transactions.push({
        id: Date.now().toString(),
        type: 'income',
        amount: sale.total,
        description: `بيع #${saleId}`,
        date: new Date().toISOString(),
        paymentMethod
    });
    
    // Remove items from stock
    sale.items.forEach(item => {
        const product = store.products.find(p => p.id === item.productId);
        if (product) {
            product.quantity -= item.quantity;
        }
    });
    
    // Clear sale
    const saleIndex = store.sales.findIndex(s => s.id === saleId);
    if (saleIndex !== -1) {
        store.sales.splice(saleIndex, 1);
    }
    
    saveData();
    return true;
}

// Expense Functions
function addExpense(amount, category, description) {
    const expenseId = Date.now().toString();
    const newExpense = {
        id: expenseId,
        amount,
        category,
        description,
        date: new Date().toISOString()
    };
    
    store.expenses.push(newExpense);
    saveData();
    return newExpense;
}

// Customer Functions
function addCustomer(name, phone) {
    const customerId = Date.now().toString();
    const newCustomer = {
        id: customerId,
        name,
        phone,
        createdAt: new Date().toISOString()
    };
    
    store.customers.push(newCustomer);
    saveData();
    return newCustomer;
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('ar-EG', { 
        maximumFractionDigits: 2 
    }).format(amount);
}

// Initialize the application
window.addEventListener('DOMContentLoaded', initApp);
