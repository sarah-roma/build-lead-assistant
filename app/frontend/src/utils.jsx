export const fetchCollections = async () => {
  try {
    const res = await fetch("http://141.125.108.191:8001/List Collections/");
    const data = await res.json();
    return data.collections || [];
  } catch (err) {
    console.error(err);
    return [];
  }
};
