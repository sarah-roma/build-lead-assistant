import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";
import {
  TextInput,
  Button,
  Select,
  SelectItem,
  InlineNotification,
  InlineLoading,
} from "carbon-components-react";

export default function UploadURL() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [url, setUrl] = useState("");
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  const uploadURL = async () => {
    if (!collectionName) {
      setNotification({
        kind: "error",
        title: "No collection selected",
        subtitle: "Please choose a collection to store the URL content.",
      });
      return;
    }

    if (!url.trim()) {
      setNotification({
        kind: "error",
        title: "No URL provided",
        subtitle: "Please enter a valid URL to upload.",
      });
      return;
    }

    const formData = new FormData();
    formData.append("collection_name", collectionName);
    formData.append("url", url);

    setLoading(true); // <-- start loading
    setNotification(null);

    try {
      const res = await fetch("http://141.125.108.191:8001/Upload a URL/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok || data.status !== "success") {
        throw new Error(data.detail || "Upload failed");
      }

      setNotification({
        kind: "success",
        title: data.title,
        subtitle: data.message,
      });

      setUrl(""); // Optional UX improvement
    } catch (err) {
      console.error("UploadURL failed:", err);
      setNotification({
        kind: "error",
        title: "Upload failed",
        subtitle:
          "We couldn’t ingest the content from this URL. Please check the link and try again.",
      });
    } finally {
      setLoading(false); // <-- stop loading
    }
  };

  return (
    <div>
      <h2>Upload URL</h2>

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

      <TextInput
        id="url"
        labelText="URL"
        type="text"
        placeholder="https://example.com/article"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      {/* InlineLoading replaces button while loading */}
      {loading ? (
        <InlineLoading
          description="Uploading URL…"
          status="active"
          style={{ marginTop: "1rem" }}
        />
      ) : (
        <Button onClick={uploadURL}>Upload</Button>
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
