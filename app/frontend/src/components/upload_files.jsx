import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";
import {
  Button,
  FileUploader,
  Select,
  SelectItem,
  InlineNotification,
  InlineLoading
} from "carbon-components-react";

export default function UploadFiles() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [files, setFiles] = useState([]);
  const [notification, setNotification] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  const uploadFiles = async () => {
    if (!files.length || !collectionName) {
      setNotification({
        kind: "error",
        title: "Missing information",
        subtitle: "Please select a collection and at least one file.",
      });
      return;
    }

    const formData = new FormData();
    files.forEach((file) => formData.append("file", file));
    formData.append("collection_name", collectionName);

    setUploading(true);
    setNotification(null);

    try {
      const res = await fetch("http://localhost:8000/Upload Files/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setNotification({
        kind: "success",
        title: "Files uploaded successfully",
        subtitle: `${files.length} file(s) were added to "${collectionName}".`,
      });

      // IMPORTANT: reset uploader state so spinner clears
      setFiles([]);
    } catch (err) {
      console.error("UploadFiles failed:", err);
      setNotification({
        kind: "error",
        title: "Upload failed",
        subtitle:
          "We couldn’t process the selected files. Please check the file types and try again.",
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2>Upload Files</h2>

      <Select
        id="collection-select"
        labelText="Select a collection"
        value={collectionName}
        onChange={(e) => setCollectionName(e.target.value)}
      >
        {collections.map((col, idx) => (
          <SelectItem key={idx} value={col} text={col} />
        ))}
      </Select>

      <FileUploader
        accept={[".pdf", ".txt", ".docx"]}
        buttonLabel="Add files"
        labelDescription="Drag and drop files here or click to upload"
        multiple
        onChange={(event) => setFiles(Array.from(event.target.files))}
        filenameStatus={uploading ? "uploading" : "edit"}
      />

      {uploading ? (
        <InlineLoading
          description="Uploading files…"
          status="active"
        />
      ) : (
        <Button
          onClick={uploadFiles}
          kind="primary"
        >
          Upload
        </Button>
      )}


      {notification && (
        <InlineNotification
          kind={notification.kind}
          title={notification.title}
          subtitle={notification.subtitle}
          onCloseButtonClick={() => setNotification(null)}
        />
      )}
    </div>
  );
}
