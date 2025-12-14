import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";


export default function UploadMuralBoard() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  // Mural board URL input
  const [url, setUrl] = useState("");
  const [message, setMessage] = useState("");

  // Load collections when the component mounts and default to the first
  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  // Send the mural URL to the backend. The endpoint will handle fetching
  // and extracting content from the mural board.
  const uploadMural = async () => {
    if (!collectionName) return setMessage("Select a collection");
    try {
      const res = await fetch(
        `http://localhost:8000/Upload a Mural Board/?collection_name=${encodeURIComponent(collectionName)}&url=${encodeURIComponent(url)}`
      );
      const data = await res.json();
      setMessage(JSON.stringify(data, null, 2));
    } catch (err) {
        console.error("UploadMuralBoard failed:", err);
        setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Upload Mural Board</h2>
      {/* Collection selector */}
      <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
      </select>
      {/* URL input for MURAL board */}
      <input
        type="text"
        placeholder="Mural Board URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button onClick={uploadMural}>Upload</button>
      <pre>{message}</pre>
    </div>
  );
}