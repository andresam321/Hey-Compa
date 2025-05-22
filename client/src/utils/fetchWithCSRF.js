// 🧠 Helper function to get a cookie value by name
export function getCookie(name) {
    // 🍪 Get the string of all cookies in the browser
    const cookieStr = document.cookie;
  
    // 🔪 Split cookies into an array of individual cookies
    const cookies = cookieStr.split(';');
  
    // 🔁 Loop through each cookie
    for (let cookie of cookies) {
      // 🧼 Clean whitespace, then split "key=value" into key and value
      const [key, value] = cookie.trim().split('=');
  
      // ✅ If the cookie matches the one we're looking for (e.g. "csrf_token"), return its value
      if (key === name) return decodeURIComponent(value);
    }
  
    // ❌ If no match is found, return null
    return null;
  }
  
  // 📡 Wrapper function around fetch to automatically include CSRF protection
 export async function fetchWithCSRF(url, options = {}) {
  const csrfToken = getCookie("csrf_token");

  const isFormData = options.body instanceof FormData;

  const headers = {
    ...options.headers,
    ...(isFormData
      ? {} // Don't set Content-Type for FormData
      : { "Content-Type": "application/json" }),
    "X-CSRFToken": csrfToken,
  };

  return fetch(url, {
    ...options,
    headers,
    credentials: "include",
  });
}
  