import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";
import {
  Button,
  TextInput,
  Select,
  SelectItem,
  InlineNotification,
  InlineLoading, // <-- import InlineLoading
} from "carbon-components-react";

export default function AskQuestion() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
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

  const askQuestion = async () => {
    if (!collectionName || !question) {
      setNotification({
        kind: "error",
        title: "Missing information",
        subtitle: "Please select a collection and enter a question.",
      });
      return;
    }

    setLoading(true);
    setAnswer("");
    setNotification(null);

    try {
      const res = await fetch(
        `http://51.15.73.99:8001/Ask a Question/?collection_name=${encodeURIComponent(
          collectionName
        )}&question=${encodeURIComponent(question)}`,
        { method: "POST" }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setAnswer(data.answer);

    } catch (err) {
      console.error("AskQuestion failed:", err);
      setNotification({
        kind: "error",
        title: "Unable to answer question",
        subtitle:
          "Something went wrong while retrieving an answer. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Ask a Question</h2>

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
        id="question-input"
        labelText="Your question"
        placeholder="Type your question here"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      {/* InlineLoading replaces the button while loading */}
      {loading ? (
        <InlineLoading
          description="Searching…"
          status="active"
          style={{ marginTop: "1rem" }}
        />
      ) : (
        <Button
          onClick={askQuestion}
          kind="primary"
        >
          Ask
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

      {answer && (
        <div style={{ marginTop: "1.5rem" }}>
          <h4>Answer:</h4>
          <p style={{ whiteSpace: "pre-line" }}>{answer}</p>
        </div>
      )}
    </div>
  );
}
