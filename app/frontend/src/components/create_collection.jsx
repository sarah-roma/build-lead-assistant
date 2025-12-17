import { useState } from "react";
import { TextInput, Button, InlineNotification } from "carbon-components-react";


export default function CreateCollection() {
  // The value entered by the user for the new collection's name.
  const [collectionName, setCollectionName] = useState("");
  // Small message area used to show validation or server responses.
  const [message, setMessage] = useState("");

  // Handler that validates the input and calls the backend to create a
  // collection. It catches network errors and writes a brief message for UI.
  const createCollection = async () => {
    if (!collectionName) return setMessage("Enter a collection name");

    try {
      const res = await fetch(`http://localhost:8000/Create a Collection/?collection_name=${collectionName}`, {
        method: "POST",
      });
      const data = await res.json();
      // Prefer a human-readable message from the server, otherwise show
      // the raw JSON for debugging purposes.
      setMessage(data.message || JSON.stringify(data));
    } catch (err) {
        console.error("CreateCollection failed:", err);
        setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Create Collection</h2>
      {/* Input bound to `collectionName` with an onChange handler */}
      <TextInput
        id="collection-name"
        labelText="Collection Name"
        type="text"
        placeholder="Collection Name"
        value={collectionName}
        onChange={(e) => setCollectionName(e.target.value)}
      />
      {/* Trigger collection creation when clicked */}
      <Button onClick={createCollection}>Create</Button>
      {/* Message area for validation/server responses */}
        {message && <InlineNotification
        kind="info"
        title="Message"
        subtitle={message}
      />}
    </div>
  );
}