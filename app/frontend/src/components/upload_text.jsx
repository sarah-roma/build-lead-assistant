import { useState, useEffect } from "react";
import { fetchCollections, getApiUrl } from "../utils";
import {
  TextArea,
  Button,
  Select,
  SelectItem,
  InlineNotification,
  InlineLoading,
} from "carbon-components-react";

export default function UploadText() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [information, setInformation] = useState("");
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const abortController = new AbortController();
    let isMounted = true;

    const loadCollections = async () => {
      const cols = await fetchCollections(abortController.signal);
      if (isMounted) {
        setCollections(cols);
        if (cols.length > 0) setCollectionName(cols[0]);
      }
    };

    loadCollections();

    return () => {
      isMounted = false;
      abortController.abort();
    };
  }, []);

  const uploadText = async () => {
    if (!collectionName) {
      setNotification({
        kind: "error",
        title: "No collection selected",
        subtitle: "Please select a collection before uploading text.",
      });
      return;
    }

    if (!information.trim()) {
      setNotification({
        kind: "error",
        title: "No text provided",
        subtitle: "Please enter some text to upload.",
      });
      return;
    }

    setLoading(true);
    setNotification(null);

    const abortController = new AbortController();

    try {
      const apiUrl = getApiUrl();
      const res = await fetch(
        `${apiUrl}/Upload Text/?collection_name=${encodeURIComponent(
          collectionName
        )}&information=${encodeURIComponent(information)}`,
        { signal: abortController.signal }
      );

      const data = await res.json();

      if (!res.ok || data.status !== "success") {
        throw new Error(data.detail || "Upload failed");
      }

      setNotification({
        kind: "success",
        title: data.title,
        subtitle: data.message,
      });

      setInformation("");
    } catch (err) {
      if (err.name !== "AbortError") {
        console.error("UploadText failed:", err);
        setNotification({
          kind: "error",
          title: "Upload failed",
          subtitle: "Something went wrong while uploading your text.",
        });
      }
    } finally {
      setLoading(false); // <-- stop loading
    }
  };

  return (
    <div>
      <h2>Upload Text</h2>

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

      <TextArea
        id="information"
        labelText="Information"
        placeholder="Information"
        value={information}
        onChange={(e) => setInformation(e.target.value)}
        rows={4}
        cols={50}
      />

      {/* InlineLoading replaces button while loading */}
      {loading ? (
        <InlineLoading
          description="Uploading text…"
          status="active"
          style={{ marginTop: "1rem" }}
        />
      ) : (
        <Button onClick={uploadText}>Upload</Button>
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
