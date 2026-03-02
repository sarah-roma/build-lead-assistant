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
// import { useState } from "react";
// import "carbon-components/css/carbon-components.min.css";
// import "./index.css";

// import {
//   SideNav,
//   SideNavItems,
//   SideNavLink,
//   HeaderName,
//   Content
// } from "carbon-components-react";

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
//       <SideNav
//         expanded
//         isFixedNav
//         aria-label="Side navigation"
//         style={{ height: "100vh" }}
//       >
//         <HeaderName href="#" prefix="My">
//           Dashboard
//         </HeaderName>
//         <SideNavItems>
//           {tabs.map((tab) => (
//             <SideNavLink
//               key={tab.id}
//               href="#"
//               isActive={activeTab === tab.id}
//               onClick={() => setActiveTab(tab.id)}
//             >
//               {tab.label}
//             </SideNavLink>
//           ))}
//         </SideNavItems>
//         <div style={{ fontSize: "0.85rem", color: "#888", padding: "1rem" }}>
//           &copy; {new Date().getFullYear()} Your App
//         </div>
//       </SideNav>

//       {/* Main content */}
//       <Content
//         style={{
//           flex: 1,
//           overflowY: "auto",
//           padding: "2rem",
//           display: "flex",
//           justifyContent: "center",
//         }}
//       >
//         <div style={{ width: "100%", maxWidth: "900px" }}>
//           {activeTab === "createCollection" && <CreateCollection />}
//           {activeTab === "uploadText" && <UploadText />}
//           {activeTab === "uploadURL" && <UploadURL />}
//           {activeTab === "uploadMural" && <UploadMuralBoard />}
//           {activeTab === "uploadWorkshop" && <UploadWorkshop />}
//           {activeTab === "uploadFiles" && <UploadFiles />}
//           {activeTab === "askQuestion" && <AskQuestion />}
//         </div>
//       </Content>
//     </div>
//   );
// }

// export default App;


import { useState } from "react";
import "carbon-components/css/carbon-components.min.css";

import {
  Header,
  HeaderName,
  SideNav,
  SideNavItems,
  SideNavLink,
  Content,
} from "carbon-components-react";

import CreateCollection from "./components/create_collection";
import UploadText from "./components/upload_text";
import UploadURL from "./components/upload_url";
import UploadMuralBoard from "./components/upload_mural_board";
import UploadWorkshop from "./components/upload_workshop";
import UploadFiles from "./components/upload_files";
import AskQuestion from "./components/ask_question";

const SIDE_NAV_WIDTH = 256;

// footer styling used throughout application (including login overlay)
const FOOTER_STYLE = {
  position: "fixed",
  bottom: 0,
  left: 0,
  width: "100%",
  backgroundColor: "#fafafa",
  textAlign: "center",
  padding: "0.5rem",
  fontSize: "0.85rem",
  zIndex: 10001, // higher than login overlay so it is always visible
};

function App() {
  const [activeTab, setActiveTab] = useState("createCollection");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const tabs = [
    { id: "createCollection", label: "Create Collection" },
    { id: "uploadText", label: "Upload Text" },
    { id: "uploadURL", label: "Upload URL" },
    { id: "uploadMural", label: "Upload Mural Board" },
    { id: "uploadWorkshop", label: "Upload Workshop" },
    { id: "uploadFiles", label: "Upload Files" },
    { id: "askQuestion", label: "Ask a Question" },
  ];

  const handleLogin = () => {
    if (username === "app_user" && password === "synopticproject?") {
      setIsAuthenticated(true);
    } else {
      alert("Invalid credentials");
    }
  };

  return (
    <>
      {/* AUTH BLOCKING OVERLAY */}
      {!isAuthenticated && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            backgroundColor: "rgba(0, 0, 0, 0.85)",
            zIndex: 10000,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              background: "white",
              padding: "2rem",
              borderRadius: "8px",
              width: "100%",
              maxWidth: "400px",
              textAlign: "center",
            }}
          >
            <h2 style={{ marginBottom: "1rem" }}>Restricted Access</h2>

            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleLogin()}
              style={{ width: "100%", padding: "0.5rem", marginBottom: "1rem" }}
              autoFocus
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleLogin()}
              style={{ width: "100%", padding: "0.5rem", marginBottom: "1rem" }}
            />

            <button
              style={{
                width: "100%",
                padding: "0.75rem",
                fontWeight: "bold",
                cursor: "pointer",
              }}
              onClick={handleLogin}
            >
              Enter
            </button>
          </div>
          {/* ensure login overlay doesn't hide the footer link */}
          <div style={{
            position: "relative",
            marginTop: "1rem",
            fontSize: "0.85rem",
          }}>
            <a href="https://sarah-roma.github.io/" target="_blank" rel="noopener noreferrer">
              Please visit the following site for tutorials and further information
            </a>
          </div>
        </div>
      )}

      {/* Header */}
      <Header aria-label="My Dashboard">
        <HeaderName href="#" prefix="My">
          Dashboard
        </HeaderName>

        {/* WARNING BANNER */}
        <div
          style={{
            width: "100%",
            backgroundColor: "#da1e28",
            color: "white",
            textAlign: "center",
            fontWeight: "bold",
            padding: "0.5rem",
            position: "absolute",
            top: "3rem",
            left: 0,
            zIndex: 9999,
          }}
        >
          Please do not enter any sensitive information, including client data
        </div>
      </Header>

      {/* Fixed SideNav */}
      <SideNav
        aria-label="Side navigation"
        isFixedNav
        expanded
        style={{
          top: "3rem",
          height: "calc(100vh - 3rem)",
        }}
      >
        <SideNavItems>
          {tabs.map((tab) => (
            <SideNavLink
              key={tab.id}
              href="#"
              isActive={activeTab === tab.id}
              onClick={(e) => {
                e.preventDefault();
                setActiveTab(tab.id);
              }}
            >
              {tab.label}
            </SideNavLink>
          ))}
        </SideNavItems>
      </SideNav>

      {/* Main content */}
      <main
        style={{
          marginLeft: SIDE_NAV_WIDTH,
          marginTop: "3rem",
          padding: "2rem",
        }}
      >
        <Content>
          {activeTab === "createCollection" && <CreateCollection />}
          {activeTab === "uploadText" && <UploadText />}
          {activeTab === "uploadURL" && <UploadURL />}
          {activeTab === "uploadMural" && <UploadMuralBoard />}
          {activeTab === "uploadWorkshop" && <UploadWorkshop />}
          {activeTab === "uploadFiles" && <UploadFiles />}
          {activeTab === "askQuestion" && <AskQuestion />}
        </Content>
      </main>

      {/* persistent footer that stays at bottom of viewport */}
      <div style={FOOTER_STYLE}>
        Please visit the following site for tutorials and further information:&nbsp;
        <a href="https://sarah-roma.github.io/" target="_blank" rel="noopener noreferrer">
          https://sarah-roma.github.io/
        </a>
      </div>
    </>
  );
}

export default App;