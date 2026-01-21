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

const API_BASE = "http://localhost:8001";

export default function UploadMuralBoard() {
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

  /**
   * Single upload attempt
   */
  const attemptUpload = async () => {
    const res = await fetch(
      `${API_BASE}/Upload a Mural Board/?collection_name=${encodeURIComponent(
        collectionName
      )}&url=${encodeURIComponent(url)}`
    );

    const data = await res.json();

    // OAuth required
    if (res.status === 401 && data.authorization_url) {
      window.open(data.authorization_url, "_blank");
      throw new Error("AUTH_REQUIRED");
    }

    if (!res.ok || data.status !== "success") {
      throw new Error(data.detail || "Upload failed");
    }

    return data;
  };

  /**
   * Main handler
   */
  const uploadMural = async () => {
    if (!collectionName) {
      setNotification({
        kind: "error",
        title: "No collection selected",
        subtitle: "Please choose a collection to store the Mural board content.",
      });
      return;
    }

    if (!url.trim()) {
      setNotification({
        kind: "error",
        title: "No Mural URL provided",
        subtitle: "Please enter a valid Mural board URL.",
      });
      return;
    }

    setLoading(true);
    setNotification(null);

    try {
      let data;

      try {
        // First attempt
        data = await attemptUpload();
      } catch (err) {
        if (err.message === "AUTH_REQUIRED") {
          // Wait briefly for OAuth to complete
          await new Promise((resolve) => setTimeout(resolve, 1500));

          // Retry once
          data = await attemptUpload();
        } else {
          throw err;
        }
      }

      setNotification({
        kind: "success",
        title: data.title,
        subtitle: data.message,
      });

      setUrl("");
    } catch (err) {
      console.error("UploadMuralBoard failed:", err);
      setNotification({
        kind: "error",
        title: "Upload failed",
        subtitle:
          "We couldn’t ingest data from this Mural board. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Upload Mural Board</h2>

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
        id="mural-url"
        labelText="Mural Board URL"
        type="text"
        placeholder="https://app.mural.co/..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      {loading ? (
        <InlineLoading
          description="Uploading Mural board…"
          status="active"
          style={{ marginTop: "1rem" }}
        />
      ) : (
        <Button onClick={uploadMural}>Upload</Button>
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
