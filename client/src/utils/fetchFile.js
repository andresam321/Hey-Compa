export const fetchFile = async (url, formData, options = {}) => {
  return fetch(url, {
    method: "POST",
    body: formData,
    credentials: "include",
    ...options,
  });
};
