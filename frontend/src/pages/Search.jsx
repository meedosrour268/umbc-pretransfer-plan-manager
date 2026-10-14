import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function SearchPage() {
  const apiBase = useMemo(
    () => import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
    []
  );
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function search(event) {
    event?.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    try {
      const response = await fetch(
        `${apiBase}/search?query=${encodeURIComponent(query.trim())}`
      );
      if (response.status === 401) {
        setError("Google Drive is not connected yet.");
        setResults([]);
        return;
      }
      if (!response.ok) throw new Error("Search failed");
      setResults(await response.json());
    } catch {
      setError("Could not search Google Drive. Make sure the API is running.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero">
        <span className="eyebrow">CMSC 447 PORTFOLIO PROJECT</span>
        <h1>UMBC Pre-Transfer Plan Manager</h1>
        <p>
          Search advising plans stored in Google Drive, preview a selected plan,
          and export it as PDF or Word.
        </p>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Student plan search</h2>
            <p>Search Google Docs by student or plan name.</p>
          </div>
          <a className="secondary-button" href={`${apiBase}/authorize`}>
            Connect Google Drive
          </a>
        </div>

        <form className="search-row" onSubmit={search}>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Try: Tester, Paul"
            aria-label="Search student plans"
          />
          <button type="submit" disabled={loading || !query.trim()}>
            {loading ? "Searching…" : "Search"}
          </button>
        </form>

        {error && <div className="message error">{error}</div>}

        <div className="results">
          {results.map((doc) => (
            <button
              className="result-card"
              key={doc.id}
              onClick={() =>
                navigate("/preview", { state: { id: doc.id, name: doc.name } })
              }
            >
              <span>
                <strong>{doc.name}</strong>
                <small>
                  Modified {doc.modifiedTime ? new Date(doc.modifiedTime).toLocaleString() : "N/A"}
                </small>
              </span>
              <span className="arrow">→</span>
            </button>
          ))}
        </div>

        {!loading && !error && results.length === 0 && (
          <div className="empty-state">
            Search results will appear here after Google Drive is connected.
          </div>
        )}
      </section>
    </main>
  );
}
