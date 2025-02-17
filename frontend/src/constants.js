import API_BASE_URL from "./config";

export const API_ENDPOINTS = {
  ROOT: `${API_BASE_URL}/`,
  LOGIN: `${API_BASE_URL}/auth/login`,
  REGISTER: `${API_BASE_URL}/auth/register`,
  USERS: `${API_BASE_URL}/users`,
  PRODUCTS: `${API_BASE_URL}/products`,
  ORDERS: `${API_BASE_URL}/orders`,
  CART: `${API_BASE_URL}/cart`,
  CHECKOUT: `${API_BASE_URL}/checkout`,
  ANALYTICS: `${API_BASE_URL}/analytics`,
  REPORTS: `${API_BASE_URL}/reports`,
};

export default API_ENDPOINTS;

