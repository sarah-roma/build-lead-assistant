export const fetchCollections = async () => {
  try {
    const res = await fetch("http://localhost:8000/List Collections/");
    const data = await res.json();
    return data.collections || [];
  } catch (err) {
    console.error(err);
    return [];
  }
};
