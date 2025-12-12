import { useState } from "react";

export default function CreateCollection() {
  const [collectionName, setCollectionName] = useState("");
  const [message, setMessage] = useState("");

  const createCollection = async () => {
    if (!collectionName) return setMessage("Enter a collection name");

    try {
      const res = await fetch(`http://localhost:8000/Create a Collection/?collection_name=${collectionName}`, {
        method: "POST",
      });
      const data = await res.json();
      setMessage(data.message || JSON.stringify(data));
    } catch (err) {
      setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Create Collection</h2>
      <input
        type="text"
        placeholder="Collection Name"
        value={collectionName}
        onChange={(e) => setCollectionName(e.target.value)}
      />
      <button onClick={createCollection}>Create</button>
      <p>{message}</p>
    </div>
  );
}