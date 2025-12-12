import { useState } from "react";
import { fetchCollections } from "../utils";

export default function UploadText() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [information, setInformation] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  const uploadText = async () => {
    if (!collectionName) return setMessage("Select a collection");
    try {
      const res = await fetch(
        `http://localhost:8000/Upload Text/?collection_name=${encodeURIComponent(collectionName)}&information=${encodeURIComponent(information)}`
      );
      const data = await res.json();
      setMessage(JSON.stringify(data, null, 2));
    } catch (err) {
      setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Upload Text</h2>
      <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
      </select>
      <textarea
        placeholder="Information"
        value={information}
        onChange={(e) => setInformation(e.target.value)}
        rows={4}
        cols={50}
      />
      <button onClick={uploadText}>Upload</button>
      <pre>{message}</pre>
    </div>
  );
}
