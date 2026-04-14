const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001";

export const fetchCollections = async (signal) => {
  try {
    const res = await fetch(`${API_URL}/List Collections/`, { signal });
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    return data.collections || [];
  } catch (err) {
    if (err.name !== "AbortError") {
      console.error("Error fetching collections:", err);
    }
    return [];
  }
};

export const getApiUrl = () => API_URL;
