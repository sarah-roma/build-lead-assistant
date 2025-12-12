import { useState } from "react";
import { fetchCollections } from "../utils";

export default function UploadFiles() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [files, setFiles] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  const handleFileChange = (e) => setFiles(e.target.files);

  const uploadFiles = async () => {
    if (!files || !collectionName) return setMessage("Select a collection and files");
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) formData.append("file", files[i]);
    formData.append("collection_name", collectionName);

    try {
      const res = await fetch(`http://localhost:8000/Upload Files/`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setMessage(JSON.stringify(data, null, 2));
    } catch (err) {
      setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Upload Files</h2>
      <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
      </select>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={uploadFiles}>Upload</button>
      <pre>{message}</pre>
    </div>
  );
}