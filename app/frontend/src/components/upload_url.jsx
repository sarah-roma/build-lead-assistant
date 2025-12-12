import { useState } from "react";
import { fetchCollections } from "../utils";

export default function UploadURL() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [url, setUrl] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  const uploadURL = async () => {
    if (!collectionName) return setMessage("Select a collection");
    try {
      const res = await fetch(
        `http://localhost:8000/Upload a URL/?collection_name=${encodeURIComponent(collectionName)}&url=${encodeURIComponent(url)}`
      );
      const data = await res.json();
      setMessage(JSON.stringify(data, null, 2));
    } catch (err) {
      setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Upload URL</h2>
      <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
      </select>
      <input
        type="text"
        placeholder="URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button onClick={uploadURL}>Upload</button>
      <pre>{message}</pre>
    </div>
  );
}