// Used the following commands:
// npm create vite@latest frontend --template react
// cd frontend
// npm install


// I originally had one big file with all the components but then I split it up for better
// modularity and maintainability and also to make it more reusable and easier to test

// React hook for local component state and global stylesheet
// import { useState } from "react";
// import "carbon-components/css/carbon-components.min.css";
// import "./index.css";

// // Import the individual dashboard panels (each panel is a small, focused component)
// import CreateCollection from "./components/create_collection";
// import UploadText from "./components/upload_text";
// import UploadURL from "./components/upload_url";
// import UploadMuralBoard from "./components/upload_mural_board";
// import UploadWorkshop from "./components/upload_workshop";
// import UploadFiles from "./components/upload_files";
// import AskQuestion from "./components/ask_question";

// function App() {
//   // `activeTab` holds the id of the currently visible panel. `setActiveTab`
//   // is used by the sidebar buttons to switch which component is displayed.
//   const [activeTab, setActiveTab] = useState("createCollection");

//   // Define the available tabs for the sidebar navigation. Each tab has a unique
//   // `id` (used in logic) and a `label` (displayed to the user).
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
//     <div style={{ display: "flex", height: "100%" }}>
//       {/* Sidebar */}
//       <aside className="sidebar">
//         <div>
//           <h2>Dashboard</h2>
//           <ul>
//             {tabs.map((tab) => (
//               <li key={tab.id}>
//                 <button
//                   // Clicking a button sets the active tab id which controls
//                   // which main panel is rendered below.
//                   onClick={() => setActiveTab(tab.id)}
//                   // Add an "active" CSS class when this tab is selected so
//                   // it can be styled differently in `index.css`.
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
//           {/* Only render the currently active panel to keep the UI focused
//               and to avoid mounting all components at once. */}
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

// // Export the App component as the default export for the bundle entry point.
// export default App;
import { useState } from "react";
import "carbon-components/css/carbon-components.min.css";
import "./index.css";

import {
  SideNav,
  SideNavItems,
  SideNavLink,
  HeaderName,
  Content
} from "carbon-components-react";

import CreateCollection from "./components/create_collection";
import UploadText from "./components/upload_text";
import UploadURL from "./components/upload_url";
import UploadMuralBoard from "./components/upload_mural_board";
import UploadWorkshop from "./components/upload_workshop";
import UploadFiles from "./components/upload_files";
import AskQuestion from "./components/ask_question";

function App() {
  const [activeTab, setActiveTab] = useState("createCollection");

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
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar */}
      <SideNav
        expanded
        isFixedNav
        aria-label="Side navigation"
        style={{ height: "100vh" }}
      >
        <HeaderName href="#" prefix="My">
          Dashboard
        </HeaderName>
        <SideNavItems>
          {tabs.map((tab) => (
            <SideNavLink
              key={tab.id}
              href="#"
              isActive={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </SideNavLink>
          ))}
        </SideNavItems>
        <div style={{ fontSize: "0.85rem", color: "#888", padding: "1rem" }}>
          &copy; {new Date().getFullYear()} Your App
        </div>
      </SideNav>

      {/* Main content */}
      <Content
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "2rem",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div style={{ width: "100%", maxWidth: "900px" }}>
          {activeTab === "createCollection" && <CreateCollection />}
          {activeTab === "uploadText" && <UploadText />}
          {activeTab === "uploadURL" && <UploadURL />}
          {activeTab === "uploadMural" && <UploadMuralBoard />}
          {activeTab === "uploadWorkshop" && <UploadWorkshop />}
          {activeTab === "uploadFiles" && <UploadFiles />}
          {activeTab === "askQuestion" && <AskQuestion />}
        </div>
      </Content>
    </div>
  );
}

export default App;
