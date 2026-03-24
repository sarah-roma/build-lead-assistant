export const fetchCollections = async () => {
  try {
    const res = await fetch("http://141.125.162.121:8001/List Collections/");
    const data = await res.json();
    return data.collections || [];
  } catch (err) {
    console.error(err);
    return [];
  }
};
