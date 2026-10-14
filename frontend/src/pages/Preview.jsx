import { useLocation, useNavigate } from "react-router-dom";

export default function PreviewPage() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const apiBase = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
  const id = state?.id;
  const name = state?.name;

  if (!id) {
    return (
      <main className="page-shell">
        <section className="panel compact-panel">
          <h2>No plan selected</h2>
          <p>Return to the search page and choose a document.</p>
          <button onClick={() => navigate("/")}>Back to search</button>
        </section>
      </main>
    );
  }

  const previewUrl = `https://docs.google.com/document/d/${id}/preview`;

  return (
    <main className="page-shell preview-shell">
      <div className="preview-toolbar">
        <div>
          <button className="text-button" onClick={() => navigate(-1)}>
            ← Back
          </button>
          <h1>{name || "Student advising plan"}</h1>
        </div>
        <div className="button-group">
          <a
            className="secondary-button"
            href={`${apiBase}/generate?file_id=${encodeURIComponent(id)}&format=pdf`}
            target="_blank"
            rel="noreferrer"
          >
            Export PDF
          </a>
          <a
            className="primary-link"
            href={`${apiBase}/generate?file_id=${encodeURIComponent(id)}&format=docx`}
            target="_blank"
            rel="noreferrer"
          >
            Export Word
          </a>
        </div>
      </div>

      <section className="document-frame">
        <iframe title={name || "Google Doc preview"} src={previewUrl} />
      </section>
    </main>
  );
}
