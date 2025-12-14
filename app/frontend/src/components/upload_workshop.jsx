// import { useState, useEffect } from "react";
// import { fetchCollections } from "../utils";

// // Not showing as all the form stuff in react

// export default function UploadWorkshop() {
//   const [collections, setCollections] = useState([]);
//   const [collectionName, setCollectionName] = useState("");
//   // The workshop information entered by the user
//   const [workshopInfo, setWorkshopInfo] = useState("");
//   const [message, setMessage] = useState("");

//   // Load the available collections on mount and choose the first by default
//   useEffect(() => {
//     const loadCollections = async () => {
//       const cols = await fetchCollections();
//       setCollections(cols);
//       if (cols.length > 0) setCollectionName(cols[0]);
//     };
//     loadCollections();
//   }, []);

//   // Send workshop info as JSON in a POST request. Show network/server responses
//   // in the `message` area to help with debugging while developing.
//   const uploadWorkshop = async () => {
//     if (!collectionName) return setMessage("Select a collection");
//     try {
//       const res = await fetch(`http://localhost:8000/Upload Workshop Information/`, {
//         method: "POST",
//         body: JSON.stringify({ collection_name: collectionName, workshop_info: workshopInfo }),
//         headers: { "Content-Type": "application/json" },
//       });
//       const data = await res.json();
//       setMessage(JSON.stringify(data, null, 2));
//     } catch (err) {
//         console.error("UploadWorkshop failed:", err);
//         setMessage("Network error");
//     }
//   };

//   return (
//     <div>
//       <h2>Upload Workshop Info</h2>
//       <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
//         {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
//       </select>
//       <textarea
//         placeholder="Workshop Info"
//         value={workshopInfo}
//         onChange={(e) => setWorkshopInfo(e.target.value)}
//         rows={4}
//         cols={50}
//       />
//       <button onClick={uploadWorkshop}>Upload</button>
//       <pre>{message}</pre>
//     </div>
//   );
// }

// getting lots of JSON vs FormData mismatch errors
import { useState, useEffect } from "react";
import { fetchCollections } from "../utils";

export default function UploadWorkshop() {
  const [collections, setCollections] = useState([]);
  const [collectionName, setCollectionName] = useState("");

  const [workshopDate, setWorkshopDate] = useState("");
  const [muralUrl, setMuralUrl] = useState("");

  const [attendees, setAttendees] = useState([
    { name: "", job_title: "", team: "", company: "" }
  ]);

//   const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  /* --------------------------------------------------
     Load collections on mount
  -------------------------------------------------- */
  useEffect(() => {
    const loadCollections = async () => {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0) setCollectionName(cols[0]);
    };
    loadCollections();
  }, []);

  /* --------------------------------------------------
     Attendee helpers
  -------------------------------------------------- */
  const updateAttendee = (index, field, value) => {
    const updated = [...attendees];
    updated[index][field] = value;
    setAttendees(updated);
  };

  const addAttendee = () => {
    setAttendees([...attendees, { name: "", job_title: "", team: "", company: "" }]);
  };

  const removeAttendee = (index) => {
    setAttendees(attendees.filter((_, i) => i !== index));
  };

  /* --------------------------------------------------
     Submit workshop
  -------------------------------------------------- */
  const uploadWorkshop = async () => {
    if (!collectionName) {
      setMessage("Select a collection");
      return;
    }

    const formData = new FormData();
    formData.append("collection_name", collectionName);

    // FastAPI query parameter
    const url = "http://localhost:8000/Upload Workshop Information/";


    // Form fields
    if (workshopDate) formData.append("workshop_date", workshopDate);
    if (muralUrl) formData.append("mural_url", muralUrl);

    // Repeatable attendee fields
    attendees.forEach((a) => {
      if (a.name) {
        formData.append("attendee_names", a.name);
        formData.append("attendee_job_titles", a.job_title);
        formData.append("attendee_teams", a.team);
        formData.append("attendee_companies", a.company);
      }
    });

    // // Optional file
    // if (file) {
    //   formData.append("workshop_files", file);
    // }

    try {
      const res = await fetch(url, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setMessage(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error("UploadWorkshop failed:", err);
      setMessage("Network error");
    }
  };

  /* --------------------------------------------------
     UI
  -------------------------------------------------- */
  return (
    <div>
      <h2>Upload Workshop Information</h2>

      {/* Collection */}
      <label>
        Collection:
        <select
          value={collectionName}
          onChange={(e) => setCollectionName(e.target.value)}
        >
          {collections.map((col, idx) => (
            <option key={idx} value={col}>{col}</option>
          ))}
        </select>
      </label>

      <hr />

      {/* Workshop date */}
      <label>
        Workshop Date:
        <input
          type="text"
          placeholder="e.g. 12 March 2024"
          value={workshopDate}
          onChange={(e) => setWorkshopDate(e.target.value)}
        />
      </label>

      {/* Mural URL */}
      <label>
        Mural URL:
        <input
          type="text"
          placeholder="https://app.mural.co/..."
          value={muralUrl}
          onChange={(e) => setMuralUrl(e.target.value)}
        />
      </label>

      <hr />

      {/* Attendees */}
      <h3>Attendees</h3>

      {attendees.map((a, idx) => (
        <div key={idx} style={{ border: "1px solid #ddd", padding: "1rem", marginBottom: "1rem" }}>
          <input
            placeholder="Name"
            value={a.name}
            onChange={(e) => updateAttendee(idx, "name", e.target.value)}
          />
          <input
            placeholder="Job Title"
            value={a.job_title}
            onChange={(e) => updateAttendee(idx, "job_title", e.target.value)}
          />
          <input
            placeholder="Team"
            value={a.team}
            onChange={(e) => updateAttendee(idx, "team", e.target.value)}
          />
          <input
            placeholder="Company"
            value={a.company}
            onChange={(e) => updateAttendee(idx, "company", e.target.value)}
          />

          {attendees.length > 1 && (
            <button onClick={() => removeAttendee(idx)}>Remove</button>
          )}
        </div>
      ))}

      <button onClick={addAttendee}>Add Attendee</button>

      <button onClick={uploadWorkshop}>Upload Workshop</button>

      <pre>{message}</pre>
    </div>
  );
}

//       <hr />

//      {/* File upload */}
//      <label>
//        Upload Workshop File:
//        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
//      </label>

//      <hr />