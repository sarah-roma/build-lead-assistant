import { useState } from "react";
import { fetchCollections } from "../utils";

export default function UploadWorkshop() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [workshopInfo, setWorkshopInfo] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  const uploadWorkshop = async () => {
    if (!collectionName) return setMessage("Select a collection");
    try {
      const res = await fetch(`http://localhost:8000/Upload Workshop Information/`, {
        method: "POST",
        body: JSON.stringify({ collection_name: collectionName, workshop_info: workshopInfo }),
        headers: { "Content-Type": "application/json" },
      });
      const data = await res.json();
      setMessage(JSON.stringify(data, null, 2));
    } catch (err) {
      setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Upload Workshop Info</h2>
      <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
      </select>
      <textarea
        placeholder="Workshop Info"
        value={workshopInfo}
        onChange={(e) => setWorkshopInfo(e.target.value)}
        rows={4}
        cols={50}
      />
      <button onClick={uploadWorkshop}>Upload</button>
      <pre>{message}</pre>
    </div>
  );
}