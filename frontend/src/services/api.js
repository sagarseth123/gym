// frontend/src/services/api.js
const BASE_URL = 'http://localhost:8000'; // Adjust if your backend URL is different

export const adminSignup = async (userData) => {
  const payload = {
    full_name: userData.fullName,
    email: userData.email,
    hashed_password: userData.password, // Backend expects 'hashed_password' for plain pass on UserCreate
    role: 'admin', // Role is set by backend, but UserCreate model allows it
    is_active: true // Default, can be omitted if backend handles it
  };

  const response = await fetch(`${BASE_URL}/auth/signup/admin`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    // Try to parse error JSON, otherwise use a generic message from statusText
    let errorDetail = `Signup failed: ${response.statusText}`;
    try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorDetail;
    } catch (e) {
        // Ignore if response is not JSON or already handled by statusText
    }
    throw new Error(errorDetail);
  }
  return response.json();
};

export const adminLogin = async (credentials) => {
  const formData = new URLSearchParams();
  formData.append('username', credentials.email); // FastAPI's OAuth2PasswordRequestForm uses 'username'
  formData.append('password', credentials.password);

  const response = await fetch(`${BASE_URL}/auth/login/admin`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });

  if (!response.ok) {
    // Try to parse error JSON, otherwise use a generic message from statusText
    let errorDetail = `Login failed: ${response.statusText}`;
    try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorDetail;
    } catch (e) {
        // Ignore if response is not JSON
    }
    throw new Error(errorDetail);
  }
  return response.json(); // This will contain the access_token
};
