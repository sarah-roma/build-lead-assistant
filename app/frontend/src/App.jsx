// import { useState, useEffect } from "react";

// // --- Helper to fetch collections ---
// const fetchCollections = async () => {
//   try {
//     const res = await fetch("http://localhost:8000/List Collections/");
//     const data = await res.json();
//     return data.collections || [];
//   } catch (err) {
//     console.error("Error fetching collections", err);
//     return [];
//   }
// };

// --- 1. Create Collection ---
// function CreateCollection() {
//   const [collectionName, setCollectionName] = useState("");
//   const [message, setMessage] = useState("");

//   const createCollection = async () => {
//     if (!collectionName) return setMessage("Enter a collection name");

//     try {
//       const res = await fetch(`http://localhost:8000/Create a Collection/?collection_name=${collectionName}`, {
//         method: "POST",
//       });
//       const data = await res.json();
//       setMessage(data.message || JSON.stringify(data));
//     } catch (err) {
//       setMessage("Network error");
//     }
//   };

//   return (
//     <div>
//       <h2>Create Collection</h2>
//       <input
//         type="text"
//         placeholder="Collection Name"
//         value={collectionName}
//         onChange={(e) => setCollectionName(e.target.value)}
//       />
//       <button onClick={createCollection}>Create</button>
//       <p>{message}</p>
//     </div>
//   );
// }

// --- 2. Upload Text ---
// function UploadText() {
//   const [collections, setCollections] = useState([]);
//   const [collectionName, setCollectionName] = useState("");
//   const [information, setInformation] = useState("");
//   const [message, setMessage] = useState("");

//   useEffect(() => {
//     const loadCollections = async () => {
//       const cols = await fetchCollections();
//       setCollections(cols);
//       if (cols.length > 0) setCollectionName(cols[0]);
//     };
//     loadCollections();
//   }, []);

//   const uploadText = async () => {
//     if (!collectionName) return setMessage("Select a collection");
//     try {
//       const res = await fetch(
//         `http://localhost:8000/Upload Text/?collection_name=${encodeURIComponent(collectionName)}&information=${encodeURIComponent(information)}`
//       );
//       const data = await res.json();
//       setMessage(JSON.stringify(data, null, 2));
//     } catch (err) {
//       setMessage("Network error");
//     }
//   };

//   return (
//     <div>
//       <h2>Upload Text</h2>
//       <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
//         {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
//       </select>
//       <textarea
//         placeholder="Information"
//         value={information}
//         onChange={(e) => setInformation(e.target.value)}
//         rows={4}
//         cols={50}
//       />
//       <button onClick={uploadText}>Upload</button>
//       <pre>{message}</pre>
//     </div>
//   );
// }

// --- 3. Upload URL ---
// function UploadURL() {
//   const [collections, setCollections] = useState([]);
//   const [collectionName, setCollectionName] = useState("");
//   const [url, setUrl] = useState("");
//   const [message, setMessage] = useState("");

//   useEffect(() => {
//     const loadCollections = async () => {
//       const cols = await fetchCollections();
//       setCollections(cols);
//       if (cols.length > 0) setCollectionName(cols[0]);
//     };
//     loadCollections();
//   }, []);

//   const uploadURL = async () => {
//     if (!collectionName) return setMessage("Select a collection");
//     try {
//       const res = await fetch(
//         `http://localhost:8000/Upload a URL/?collection_name=${encodeURIComponent(collectionName)}&url=${encodeURIComponent(url)}`
//       );
//       const data = await res.json();
//       setMessage(JSON.stringify(data, null, 2));
//     } catch (err) {
//       setMessage("Network error");
//     }
//   };

//   return (
//     <div>
//       <h2>Upload URL</h2>
//       <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
//         {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
//       </select>
//       <input
//         type="text"
//         placeholder="URL"
//         value={url}
//         onChange={(e) => setUrl(e.target.value)}
//       />
//       <button onClick={uploadURL}>Upload</button>
//       <pre>{message}</pre>
//     </div>
//   );
// }

// --- 4. Upload Mural Board ---
// function UploadMuralBoard() {
//   const [collections, setCollections] = useState([]);
//   const [collectionName, setCollectionName] = useState("");
//   const [url, setUrl] = useState("");
//   const [message, setMessage] = useState("");

//   useEffect(() => {
//     const loadCollections = async () => {
//       const cols = await fetchCollections();
//       setCollections(cols);
//       if (cols.length > 0) setCollectionName(cols[0]);
//     };
//     loadCollections();
//   }, []);

//   const uploadMural = async () => {
//     if (!collectionName) return setMessage("Select a collection");
//     try {
//       const res = await fetch(
//         `http://localhost:8000/Upload a Mural Board/?collection_name=${encodeURIComponent(collectionName)}&url=${encodeURIComponent(url)}`
//       );
//       const data = await res.json();
//       setMessage(JSON.stringify(data, null, 2));
//     } catch (err) {
//       setMessage("Network error");
//     }
//   };

//   return (
//     <div>
//       <h2>Upload Mural Board</h2>
//       <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
//         {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
//       </select>
//       <input
//         type="text"
//         placeholder="Mural Board URL"
//         value={url}
//         onChange={(e) => setUrl(e.target.value)}
//       />
//       <button onClick={uploadMural}>Upload</button>
//       <pre>{message}</pre>
//     </div>
//   );
// }

// --- 5. Upload Workshop Info ---
// function UploadWorkshop() {
//   const [collections, setCollections] = useState([]);
//   const [collectionName, setCollectionName] = useState("");
//   const [workshopInfo, setWorkshopInfo] = useState("");
//   const [message, setMessage] = useState("");

//   useEffect(() => {
//     const loadCollections = async () => {
//       const cols = await fetchCollections();
//       setCollections(cols);
//       if (cols.length > 0) setCollectionName(cols[0]);
//     };
//     loadCollections();
//   }, []);

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
//       setMessage("Network error");
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

// --- 6. Upload Files ---
// function UploadFiles() {
//   const [collections, setCollections] = useState([]);
//   const [collectionName, setCollectionName] = useState("");
//   const [files, setFiles] = useState(null);
//   const [message, setMessage] = useState("");

//   useEffect(() => {
//     const loadCollections = async () => {
//       const cols = await fetchCollections();
//       setCollections(cols);
//       if (cols.length > 0) setCollectionName(cols[0]);
//     };
//     loadCollections();
//   }, []);

//   const handleFileChange = (e) => setFiles(e.target.files);

//   const uploadFiles = async () => {
//     if (!files || !collectionName) return setMessage("Select a collection and files");
//     const formData = new FormData();
//     for (let i = 0; i < files.length; i++) formData.append("file", files[i]);
//     formData.append("collection_name", collectionName);

//     try {
//       const res = await fetch(`http://localhost:8000/Upload Files/`, {
//         method: "POST",
//         body: formData,
//       });
//       const data = await res.json();
//       setMessage(JSON.stringify(data, null, 2));
//     } catch (err) {
//       setMessage("Network error");
//     }
//   };

//   return (
//     <div>
//       <h2>Upload Files</h2>
//       <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
//         {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
//       </select>
//       <input type="file" multiple onChange={handleFileChange} />
//       <button onClick={uploadFiles}>Upload</button>
//       <pre>{message}</pre>
//     </div>
//   );
// }

// --- 7. Ask a Question ---
// function AskQuestion() {
//   const [collections, setCollections] = useState([]);
//   const [collectionName, setCollectionName] = useState("");
//   const [question, setQuestion] = useState("");
//   const [response, setResponse] = useState("");

//   useEffect(() => {
//     const loadCollections = async () => {
//       const cols = await fetchCollections();
//       setCollections(cols);
//       if (cols.length > 0) setCollectionName(cols[0]);
//     };
//     loadCollections();
//   }, []);

//   const askQuestion = async () => {
//     if (!collectionName) return setResponse("Select a collection");
//     try {
//       const res = await fetch(
//         `http://localhost:8000/Ask a Question/?collection_name=${encodeURIComponent(collectionName)}&question=${encodeURIComponent(question)}`,
//         { method: "POST" }
//       );
//       const data = await res.json();
//       setResponse(JSON.stringify(data, null, 2));
//     } catch (err) {
//       setResponse("Network error");
//     }
//   };

//   return (
//     <div>
//       <h2>Ask a Question</h2>
//       <select value={collectionName} onChange={(e) => setCollectionName(e.target.value)}>
//         {collections.map((col, idx) => <option key={idx} value={col}>{col}</option>)}
//       </select>
//       <input
//         type="text"
//         placeholder="Question"
//         value={question}
//         onChange={(e) => setQuestion(e.target.value)}
//       />
//       <button onClick={askQuestion}>Submit</button>
//       <pre>{response}</pre>
//     </div>
//   );
// }

// --- Main App / Dashboard ---
// function App() {
//   const [activeTab, setActiveTab] = useState("createCollection");

//   return (
//     <div style={{ display: "flex", fontFamily: "sans-serif" }}>
//       <div style={{ width: "200px", borderRight: "1px solid #ccc", padding: "1rem" }}>
//         <h3>Dashboard</h3>
//         <ul style={{ listStyle: "none", padding: 0 }}>
//           <li><button onClick={() => setActiveTab("createCollection")}>Create Collection</button></li>
//           <li><button onClick={() => setActiveTab("uploadText")}>Upload Text</button></li>
//           <li><button onClick={() => setActiveTab("uploadURL")}>Upload URL</button></li>
//           <li><button onClick={() => setActiveTab("uploadMural")}>Upload Mural Board</button></li>
//           <li><button onClick={() => setActiveTab("uploadWorkshop")}>Upload Workshop</button></li>
//           <li><button onClick={() => setActiveTab("uploadFiles")}>Upload Files</button></li>
//           <li><button onClick={() => setActiveTab("askQuestion")}>Ask a Question</button></li>
//         </ul>
//       </div>
//       <div style={{ flex: 1, padding: "1rem" }}>
//         {activeTab === "createCollection" && <CreateCollection />}
//         {activeTab === "uploadText" && <UploadText />}
//         {activeTab === "uploadURL" && <UploadURL />}
//         {activeTab === "uploadMural" && <UploadMuralBoard />}
//         {activeTab === "uploadWorkshop" && <UploadWorkshop />}
//         {activeTab === "uploadFiles" && <UploadFiles />}
//         {activeTab === "askQuestion" && <AskQuestion />}
//       </div>
//     </div>
//   );
// }

// export default App;


// import { useState } from "react";
// import CreateCollection from "./components/create_collection";
// import UploadText from "./components/upload_text";
// import UploadURL from "./components/upload_url";
// import UploadMuralBoard from "./components/upload_mural_board";
// import UploadWorkshop from "./components/upload_workshop";
// import UploadFiles from "./components/upload_files";
// import AskQuestion from "./components/ask_question";

// function App() {
//   const [activeTab, setActiveTab] = useState("createCollection");

//   const tabs = [
//     { id: "createCollection", label: "Create Collection" },
//     { id: "uploadText", label: "Upload Text" },
//     { id: "uploadURL", label: "Upload URL" },
//     { id: "uploadMural", label: "Upload Mural Board" },
//     { id: "uploadWorkshop", label: "Upload Workshop" },
//     { id: "uploadFiles", label: "Upload Files" },
//     { id: "askQuestion", label: "Ask a Question" },
//   ];

//   return (
//     <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
//       {/* Sidebar */}
//       <aside style={{ width: "250px", backgroundColor: "#f4f6f8", padding: "2rem 1rem", boxShadow: "2px 0 5px rgba(0,0,0,0.05)" }}>
//         <h2 style={{ fontSize: "1.5rem", marginBottom: "1.5rem" }}>Dashboard</h2>
//         <ul style={{ listStyle: "none", padding: 0 }}>
//           {tabs.map((tab) => (
//             <li key={tab.id} style={{ marginBottom: "1rem" }}>
//               <button
//                 onClick={() => setActiveTab(tab.id)}
//                 style={{
//                   width: "100%",
//                   textAlign: "left",
//                   padding: "0.75rem 1rem",
//                   border: "none",
//                   borderRadius: "6px",
//                   backgroundColor: activeTab === tab.id ? "#1976d2" : "transparent",
//                   color: activeTab === tab.id ? "#fff" : "#333",
//                   fontWeight: activeTab === tab.id ? "bold" : "normal",
//                   cursor: "pointer",
//                 }}
//               >
//                 {tab.label}
//               </button>
//             </li>
//           ))}
//         </ul>
//       </aside>

//       {/* Main content */}
//       <main style={{ flex: 1, padding: "2rem", backgroundColor: "#ffffff", overflowY: "auto" }}>
//         <div style={{ maxWidth: "900px", margin: "0 auto", display: "flex", flexDirection: "column", gap: "2rem" }}>
//           {activeTab === "createCollection" && <CreateCollection />}
//           {activeTab === "uploadText" && <UploadText />}
//           {activeTab === "uploadURL" && <UploadURL />}
//           {activeTab === "uploadMural" && <UploadMuralBoard />}
//           {activeTab === "uploadWorkshop" && <UploadWorkshop />}
//           {activeTab === "uploadFiles" && <UploadFiles />}
//           {activeTab === "askQuestion" && <AskQuestion />}
//         </div>
//       </main>
//     </div>
//   );
// }

// export default App;


// import { useState } from "react";
// import "./index.css";
// import CreateCollection from "./components/create_collection";
// import UploadText from "./components/upload_text";
// import UploadURL from "./components/upload_url";
// import UploadMuralBoard from "./components/upload_mural_board";
// import UploadWorkshop from "./components/upload_workshop";
// import UploadFiles from "./components/upload_files";
// import AskQuestion from "./components/ask_question";

// function App() {
//   const [activeTab, setActiveTab] = useState("createCollection");

//   const tabs = [
//     { id: "createCollection", label: "Create Collection" },
//     { id: "uploadText", label: "Upload Text" },
//     { id: "uploadURL", label: "Upload URL" },
//     { id: "uploadMural", label: "Upload Mural Board" },
//     { id: "uploadWorkshop", label: "Upload Workshop" },
//     { id: "uploadFiles", label: "Upload Files" },
//     { id: "askQuestion", label: "Ask a Question" },
//   ];

//   return (
//     <div style={{ display: "flex", height: "100vh" }}>
//       {/* Sidebar */}
//       <aside className="sidebar">
//         <div>
//           <h2>Dashboard</h2>
//           <ul>
//             {tabs.map((tab) => (
//               <li key={tab.id}>
//                 <button
//                   onClick={() => setActiveTab(tab.id)}
//                   className={activeTab === tab.id ? "active" : ""}
//                 >
//                   {tab.label}
//                 </button>
//               </li>
//             ))}
//           </ul>
//         </div>
//         <div style={{ fontSize: "0.85rem", color: "#888" }}>
//           &copy; {new Date().getFullYear()} Your App
//         </div>
//       </aside>

//       {/* Main content */}
//       <main className="main-content">
//         <div className="main-panel">
//           {activeTab === "createCollection" && <CreateCollection />}
//           {activeTab === "uploadText" && <UploadText />}
//           {activeTab === "uploadURL" && <UploadURL />}
//           {activeTab === "uploadMural" && <UploadMuralBoard />}
//           {activeTab === "uploadWorkshop" && <UploadWorkshop />}
//           {activeTab === "uploadFiles" && <UploadFiles />}
//           {activeTab === "askQuestion" && <AskQuestion />}
//         </div>
//       </main>
//     </div>
//   );
// }

// export default App;

// Used the following commands:
// npm create vite@latest frontend --template react
// cd frontend
// npm install


// I originally had one big file with all the components but then I split it up for better
// modularity and maintainability and also to make it more reusable and easier to test

// React hook for local component state and global stylesheet
import { useState } from "react";
import "./index.css";

// Import the individual dashboard panels (each panel is a small, focused component)
import CreateCollection from "./components/create_collection";
import UploadText from "./components/upload_text";
import UploadURL from "./components/upload_url";
import UploadMuralBoard from "./components/upload_mural_board";
import UploadWorkshop from "./components/upload_workshop";
import UploadFiles from "./components/upload_files";
import AskQuestion from "./components/ask_question";

function App() {
  // `activeTab` holds the id of the currently visible panel. `setActiveTab`
  // is used by the sidebar buttons to switch which component is displayed.
  const [activeTab, setActiveTab] = useState("createCollection");

  // Define the available tabs for the sidebar navigation. Each tab has a unique
  // `id` (used in logic) and a `label` (displayed to the user).
  const tabs = [
    { id: "createCollection", label: "Create Collection" },
    { id: "uploadText", label: "Upload Text" },
    { id: "uploadURL", label: "Upload URL" },
    { id: "uploadMural", label: "Upload Mural Board" },
    { id: "uploadWorkshop", label: "Upload Workshop" },
    { id: "uploadFiles", label: "Upload Files" },
    { id: "askQuestion", label: "Ask a Question" },
  ];

  return (
    <div style={{ display: "flex", height: "100%" }}>
      {/* Sidebar */}
      <aside className="sidebar">
        <div>
          <h2>Dashboard</h2>
          <ul>
            {tabs.map((tab) => (
              <li key={tab.id}>
                <button
                  // Clicking a button sets the active tab id which controls
                  // which main panel is rendered below.
                  onClick={() => setActiveTab(tab.id)}
                  // Add an "active" CSS class when this tab is selected so
                  // it can be styled differently in `index.css`.
                  className={activeTab === tab.id ? "active" : ""}
                >
                  {tab.label}
                </button>
              </li>
            ))}
          </ul>
        </div>
        <div style={{ fontSize: "0.85rem", color: "#888" }}>
          &copy; {new Date().getFullYear()} Your App
        </div>
      </aside>

      {/* Main content */}
      <main className="main-content">
        <div className="main-panel">
          {/* Only render the currently active panel to keep the UI focused
              and to avoid mounting all components at once. */}
          {activeTab === "createCollection" && <CreateCollection />}
          {activeTab === "uploadText" && <UploadText />}
          {activeTab === "uploadURL" && <UploadURL />}
          {activeTab === "uploadMural" && <UploadMuralBoard />}
          {activeTab === "uploadWorkshop" && <UploadWorkshop />}
          {activeTab === "uploadFiles" && <UploadFiles />}
          {activeTab === "askQuestion" && <AskQuestion />}
        </div>
      </main>
    </div>
  );
}

// Export the App component as the default export for the bundle entry point.
export default App;