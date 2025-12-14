import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";


export default function AskQuestion() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  // The question text to send to the backend
  const [question, setQuestion] = useState("");
  // The response from the server (rendered as JSON for development)
  const [response, setResponse] = useState("");
  const [setMessage] = useState("");

  // Load collections once and pick the first by default
  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  // Submit the question to the backend and display the result. If no
  // collection is selected, show a friendly prompt.
  const askQuestion = async () => {
    if (!collectionName) return setResponse("Select a collection");
    try {
      const res = await fetch(
        `http://localhost:8000/Ask a Question/?collection_name=${encodeURIComponent(collectionName)}&question=${encodeURIComponent(question)}`,
        { method: "POST" }
      );
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
        console.error("AskQuestion failed:", err);
        setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Ask a Question</h2>
      {/* Select which collection to ask the question against */}
      <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
      </select>
      {/* The user's question */}
      <input
        type="text"
        placeholder="Question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={askQuestion}>Submit</button>
      {/* Server-generated response shown for debugging/review */}
      <pre>{response}</pre>
    </div>
  );
}