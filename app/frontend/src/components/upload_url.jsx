import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";
import { TextInput, Button, Select, SelectItem, InlineNotification } from "carbon-components-react";


export default function UploadURL() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  // URL text input
  const [url, setUrl] = useState("");
  // Message area for server response or errors
  const [message, setMessage] = useState("");

  // Load collections once when component mounts
  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  // Send the URL to the backend; show an error if no collection is selected
  const uploadURL = async () => {
  if (!collectionName || !url) {
    return setMessage("Select a collection and enter a URL");
  }

  const formData = new FormData();
  formData.append("collection_name", collectionName);
  formData.append("url", url);

  try {
    const res = await fetch("http://localhost:8000/Upload a URL/", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text);
    }

    const data = await res.json();
    setMessage(JSON.stringify(data, null, 2));
  } catch (err) {
    console.error("UploadURL failed:", err);
    setMessage("Upload failed");
  }
};

  return (
    <div>
      <h2>Upload URL</h2>
      {/* Choose which collection to associate the URL with */}
      <Select
        id="collection-select"
        labelText="Select a collection"
        value={collectionName}
        onChange={(e) => setCollectionName(e.target.value)}
      >
        {collections.map((col, idx) => <SelectItem key={idx} value={col} text={col} />)}
      </Select>
      {/* URL input field */}
      <TextInput
        id="url"
        labelText="URL"
        type="text"
        placeholder="URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <Button onClick={uploadURL}>Upload</Button>
      {message && <InlineNotification
        kind="info"
        title="Response"
        subtitle={message}
      />}
    </div>
  );
}