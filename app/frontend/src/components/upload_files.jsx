import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";
import { Button, FileUploader, Select, SelectItem, InlineNotification } from "carbon-components-react";

export default function UploadFiles() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  // `files` is a FileList from the input element (or null if none selected)
  const [files, setFiles] = useState(null);
  const [message, setMessage] = useState("");

  // Load collections on mount and default to first if present
  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  // Store the FileList when the user selects files
  const handleFileChange = (e) => setFiles(e.target.files);

  // Build a FormData object and POST it to the backend. We append all files
  // under the same key "file" and include the collection name as a field.
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
        console.error("UploadFiles failed:", err);
        setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Upload Files</h2>
      <Select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <SelectItem key={idx} value={col} text={col} />)}
      </Select>
      {/* Native file input, allows multiple selection */}
      <FileUploader
        accept={[".pdf", ".txt", ".docx"]}
        buttonLabel="Add Files"
        labelDescription="Drag and drop files here or click to upload"
        onChange={(event) => setFiles(Array.from(event.target.files))}
        multiple
      />
      <Button onClick={uploadFiles}>Upload</Button>
      {message && <InlineNotification kind="info" title="Response" subtitle={message} />}
    </div>
  );
}