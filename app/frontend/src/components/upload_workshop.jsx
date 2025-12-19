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

export default function UploadWorkshop() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [workshopDate, setWorkshopDate] = useState("");
  const [muralUrl, setMuralUrl] = useState("");
  const [attendees, setAttendees] = useState([
    { name: "", job_title: "", team: "", company: "" },
  ]);
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(false); // <-- added loading state

  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  const updateAttendee = (index, field, value) => {
    const updated = [...attendees];
    updated[index][field] = value;
    setAttendees(updated);
  };

  const addAttendee = () => {
    setAttendees([
      ...attendees,
      { name: "", job_title: "", team: "", company: "" },
    ]);
  };

  const removeAttendee = (index) => {
    setAttendees(attendees.filter((_, i) => i !== index));
  };

  const uploadWorkshop = async () => {
    if (!collectionName) {
      setNotification({
        kind: "error",
        title: "No collection selected",
        subtitle: "Please choose a collection to store the workshop data.",
      });
      return;
    }

    setLoading(true); // <-- start loading
    setNotification(null);

    const formData = new FormData();
    formData.append("collection_name", collectionName);

    if (workshopDate) formData.append("workshop_date", workshopDate);
    if (muralUrl) formData.append("mural_url", muralUrl);

    attendees.forEach((a) => {
      if (a.name.trim()) {
        formData.append("attendee_names", a.name);
        formData.append("attendee_job_titles", a.job_title || "");
        formData.append("attendee_teams", a.team || "");
        formData.append("attendee_companies", a.company || "");
      }
    });

    try {
      const res = await fetch(
        "http://localhost:8000/Upload Workshop Information/",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setNotification({
        kind: "success",
        title: "Workshop ingested successfully",
        subtitle: `Workshop information was added to "${collectionName}".`,
      });

      // Optional UX reset
      setWorkshopDate("");
      setMuralUrl("");
      setAttendees([{ name: "", job_title: "", team: "", company: "" }]);
    } catch (err) {
      console.error("UploadWorkshop failed:", err);
      setNotification({
        kind: "error",
        title: "Upload failed",
        subtitle:
          "We couldn’t process the workshop information. Please check the inputs and try again.",
      });
    } finally {
      setLoading(false); // <-- stop loading
    }
  };

  return (
    <div>
      <h2>Upload Workshop Information</h2>

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
        id="workshop-date"
        labelText="Workshop Date"
        placeholder="e.g. 12 March 2024"
        value={workshopDate}
        onChange={(e) => setWorkshopDate(e.target.value)}
      />

      <TextInput
        id="mural-url"
        labelText="Mural URL"
        placeholder="https://app.mural.co/..."
        value={muralUrl}
        onChange={(e) => setMuralUrl(e.target.value)}
      />

      <h3>Attendees</h3>

      {attendees.map((a, idx) => (
        <div key={idx} style={{ border: "1px solid #ddd", padding: "1rem", marginBottom: "1rem" }}>
          <TextInput
            labelText="Name"
            value={a.name}
            onChange={(e) => updateAttendee(idx, "name", e.target.value)}
          />
          <TextInput
            labelText="Job Title"
            value={a.job_title}
            onChange={(e) => updateAttendee(idx, "job_title", e.target.value)}
          />
          <TextInput
            labelText="Team"
            value={a.team}
            onChange={(e) => updateAttendee(idx, "team", e.target.value)}
          />
          <TextInput
            labelText="Company"
            value={a.company}
            onChange={(e) => updateAttendee(idx, "company", e.target.value)}
          />

          {attendees.length > 1 && (
            <Button kind="secondary" onClick={() => removeAttendee(idx)}>
              Remove Attendee
            </Button>
          )}
        </div>
      ))}

      <Button kind="tertiary" onClick={addAttendee}>
        Add Attendee
      </Button>

      {/* InlineLoading replaces the upload button while loading */}
      {loading ? (
        <InlineLoading
          description="Uploading workshop…"
          status="active"
          style={{ marginTop: "1rem" }}
        />
      ) : (
        <Button kind="primary" onClick={uploadWorkshop}>
          Upload Workshop
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
    </div>
  );
}
