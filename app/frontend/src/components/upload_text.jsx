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
  const [notification, setNotification] = useState(null);


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

  try {
    const res = await fetch(
      `http://localhost:8000/Upload Text/?collection_name=${encodeURIComponent(
        collectionName
      )}&information=${encodeURIComponent(information)}`
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

    // Optional UX improvement
    setInformation("");

  } catch (err) {
    console.error("UploadText failed:", err);
    setNotification({
      kind: "error",
      title: "Upload failed",
      subtitle: "Something went wrong while uploading your text.",
    });
  }
};


  return (
    <div>
      <h2>Upload Text</h2>
      {/* Collection selector populated by `collections` */}
      <Select
        id="collection-select"
        labelText="Select a collection"
        value={collectionName}
        onChange={(e) => setCollectionName(e.target.value)}
      >
        {collections.map((col, idx) => <SelectItem key={idx} value={col} text={col} />)}
      </Select>
      {/* Text area to collect information to upload */}
      <TextArea
        id="information"
        labelText="Information"
        placeholder="Information"
        value={information}
        onChange={(e) => setInformation(e.target.value)}
        rows={4}
        cols={50}
      />
      <Button onClick={uploadText}>Upload</Button>
      {/* Response and debug output shown nicely */}
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
