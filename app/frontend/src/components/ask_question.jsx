import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";

// Carbon components
import {
  Button,
  TextInput,
  Select,
  SelectItem,
  InlineNotification,
} from "carbon-components-react";

export default function AskQuestion() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  const askQuestion = async () => {
    if (!collectionName) return setErrorMessage("Select a collection");
    try {
      const res = await fetch(
        `http://localhost:8000/Ask a Question/?collection_name=${encodeURIComponent(
          collectionName
        )}&question=${encodeURIComponent(question)}`,
        { method: "POST" }
      );
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
      setErrorMessage("");
    } catch (err) {
      console.error("AskQuestion failed:", err);
      setErrorMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Ask a Question</h2>

      <Select
        id="collection-select"
        labelText="Select Collection"
        value={collectionName}
        onChange={(e) => setCollectionName(e.target.value)}
      >
        {collections.map((col, idx) => (
          <SelectItem key={idx} text={col} value={col} />
        ))}
      </Select>

      <TextInput
        id="question-input"
        labelText="Your Question"
        placeholder="Type your question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <Button onClick={askQuestion} kind="primary">
        Submit
      </Button>

      {errorMessage && (
        <InlineNotification
          kind="error"
          title="Error"
          subtitle={errorMessage}
          lowContrast
        />
      )}

      {response && (
        <div style={{ marginTop: "1rem" }}>
          <h4>Response:</h4>
          <pre>{response}</pre>
        </div>
      )}
    </div>
  );
}
