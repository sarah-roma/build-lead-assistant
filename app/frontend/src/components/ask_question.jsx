import { useState } from "react";
import { fetchCollections } from "../utils";

export default function AskQuestion() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

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
      setResponse("Network error");
    }
  };

  return (
    <div>
      <h2>Ask a Question</h2>
      <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
        {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
      </select>
      <input
        type="text"
        placeholder="Question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={askQuestion}>Submit</button>
      <pre>{response}</pre>
    </div>
  );
}