// API Configuration
const API_BASE_URL = '/api';

// Token management
function getAuthToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

function setAuthToken(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

function logoutUser() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.reload();
}

// API request helper - NAPRAWIONA STRUKTURA
async function apiRequest(endpoint, options = {}) {
    const token = getAuthToken();
    
    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers,
        },
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        // Handle token refresh
        if (response.status === 401 && getRefreshToken()) {
            const refreshed = await refreshToken();
            if (refreshed) {
                const newToken = getAuthToken();
                config.headers['Authorization'] = `Bearer ${newToken}`;
                return await fetch(`${API_BASE_URL}${endpoint}`, config);
            }
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || data.message || 'Wystąpił błąd');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Token refresh
async function refreshToken() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: getRefreshToken() }),
        });
        
        if (response.ok) {
            const data = await response.json();
            setAuthToken(data.access, getRefreshToken());
            return true;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
    }
    
    logoutUser();
    return false;
}

// Auth API
async function registerUser(userData) {
    return await apiRequest('/auth/register/', {
        method: 'POST',
        body: JSON.stringify(userData),
    });
}

async function loginUser(email, password) {
    // Tutaj też zmienione na apiRequest dla spójności
    return await apiRequest('/auth/login/', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    }).then(data => {
        setAuthToken(data.access, data.refresh);
        return data;
    });
}

async function getUserProfile() {
    return await apiRequest('/auth/profile/');
}

// Products API
async function getProducts(kategoria = '') {
    let url = '/produkty/';
    if (kategoria) {
        url += `?kategoria=${encodeURIComponent(kategoria)}`;
    }
    return await apiRequest(url);
}

// Cart API
async function getCart() {
    return await apiRequest('/koszyk/pobierz/');
}

async function addToCart(produktId, ilosc = 1) {
    return await apiRequest('/koszyk/dodaj/', {
        method: 'POST',
        body: JSON.stringify({ produkt_id: produktId, ilosc }),
    });
}

async function addToCartWithSize(produktId, ilosc = 1, rozmiar) {
    return await apiRequest('/koszyk/dodaj/', {
        method: 'POST',
        body: JSON.stringify({ produkt_id: produktId, ilosc, rozmiar }),
    });
}

async function updateCartItem(pozycjaId, ilosc) {
    return await apiRequest('/koszyk/aktualizuj_ilosc/', {
        method: 'POST',
        body: JSON.stringify({ pozycja_id: pozycjaId, ilosc }),
    });
}

async function removeFromCartApi(pozycjaId) {
    return await apiRequest('/koszyk/usun_pozycje/', {
        method: 'POST',
        body: JSON.stringify({ pozycja_id: pozycjaId }),
    });
}

async function clearCart() {
    return await apiRequest('/koszyk/wyczysc/', {
        method: 'POST',
    });
}

// Orders API
async function checkout(adres) {
    return await apiRequest('/zamowienia/checkout/', {
        method: 'POST',
        body: JSON.stringify({ adres }),
    });
}

async function getUserOrders() {
    return await apiRequest('/zamowienia/');
}

async function getOrderDetails(orderId) {
    return await apiRequest(`/zamowienia/${orderId}/`);
}

// Opinions API
async function getProductOpinions(produktId) {
    return await apiRequest(`/opinie/?id_product=${produktId}`);
}

async function addOpinionApi(produktId, ocena, komentarz) {
    return await apiRequest('/opinie/', {
        method: 'POST',
        body: JSON.stringify({
            id_produkt: produktId,
            ocena,
            komentarz,
        }),
    });
}

const getOpinie = getProductOpinions;

// Returns API
async function createReturn(idZamowienie, powod) {
    return await apiRequest('/zwroty/', {
        method: 'POST',
        body: JSON.stringify({
            id_zamowienie: idZamowienie,
            powod,
        }),
    });
}

async function getUserReturns() {
    return await apiRequest('/zwroty/');
}

// Admin API
async function adminGetOrdersToRealize() {
    return await apiRequest('/admin/zamowienia/do_realizacji/');
}

async function adminUpdateOrderStatus(orderId, status) {
    return await apiRequest(`/admin/zamowienia/${orderId}/zmien_status/`, {
        method: 'PATCH',
        body: JSON.stringify({ status }),
    });
}

async function adminGetReturns() {
    return await apiRequest('/admin/zwroty/');
}

async function adminApproveReturn(returnId) {
    return await apiRequest(`/admin/zwroty/${returnId}/zatwierdz/`, {
        method: 'POST',
    });
}

async function adminRejectReturn(returnId) {
    return await apiRequest(`/admin/zwroty/${returnId}/odrzuc/`, {
        method: 'POST',
    });
}

// Admin - Users API
async function adminGetUsers(statusFilter = '') {
    let url = '/admin/uzytkownicy/';
    if (statusFilter) {
        url += `?status=${statusFilter}`;
    }
    return await apiRequest(url);
}

async function adminBlockUser(userId) {
    return await apiRequest(`/admin/uzytkownicy/${userId}/zablokuj/`, {
        method: 'POST',
    });
}

async function adminUnblockUser(userId) {
    return await apiRequest(`/admin/uzytkownicy/${userId}/odblokuj/`, {
        method: 'POST',
    });
}

// Admin - Opinions API
async function adminGetOpinions() {
    return await apiRequest('/admin/opinie/');
}

async function adminDeleteOpinion(opinionId) {
    return await apiRequest(`/admin/opinie/${opinionId}/usun/`, {
        method: 'POST',
    });
}