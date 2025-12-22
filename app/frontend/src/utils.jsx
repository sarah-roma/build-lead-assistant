export const fetchCollections = async () => {
  try {
    const res = await fetch("http://51.15.73.99:8001/List Collections/");
    const data = await res.json();
    return data.collections || [];
  } catch (err) {
    console.error(err);
    return [];
  }
};
