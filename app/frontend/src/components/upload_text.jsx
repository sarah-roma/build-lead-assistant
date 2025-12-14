import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";
import { TextArea, Button, Select, SelectItem, InlineNotification } from "carbon-components-react";
// I ran a linter! I then fixed the err response handling as the variable wasnt being used
// this can definitely be used for evidence

export default function UploadText() {
  // Collections fetched from the backend so the user can choose where to upload
  const [collections, setCollections] = useState([]);
  // The currently selected collection name
  const [collectionName, setCollectionName] = useState("");
  // Text area content to upload
  const [information, setInformation] = useState("");
  // Message area to show server response or validation errors
  const [message, setMessage] = useState("");

  // On mount, load available collections and default to the first one
  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  // Trigger to upload the `information` text to the selected collection.
  // Shows a friendly message if no collection is selected or when a
  // network error occurs.
  const uploadText = async () => {
    if (!collectionName) return setMessage("Select a collection");
    try {
      const res = await fetch(
        `http://localhost:8000/Upload Text/?collection_name=${encodeURIComponent(collectionName)}&information=${encodeURIComponent(information)}`
      );
      const data = await res.json();
      setMessage(JSON.stringify(data, null, 2));
    } catch (err) {
        console.error("UploadText failed:", err);
        setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Upload Text</h2>
      {/* Collection selector populated by `collections` */}
      <Select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <SelectItem key={idx} value={col} text={col} />)}
      </Select>
      {/* Text area to collect information to upload */}
      <TextArea
        placeholder="Information"
        value={information}
        onChange={(e) => setInformation(e.target.value)}
        rows={4}
        cols={50}
      />
      <Button onClick={uploadText}>Upload</Button>
      {/* Response and debug output shown nicely */}
      {message && <InlineNotification
        kind="info"
        title="Response"
        subtitle={message}
      />}
    </div>
  );
}
