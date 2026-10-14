import { Route, Routes } from "react-router-dom";
import SearchPage from "./pages/Search.jsx";
import PreviewPage from "./pages/Preview.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<SearchPage />} />
      <Route path="/preview" element={<PreviewPage />} />
    </Routes>
  );
}
