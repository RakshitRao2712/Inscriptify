import { useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

const languageOptions = [
  { value: "", label: "Keep original language" },
  { value: "hi", label: "Translate to Hindi" },
  { value: "en", label: "Translate to English" },
];

const supportedTypes = [
  "Images",
  "PDFs",
  "Videos",
];

function App() {
  const [file, setFile] = useState(null);
  const [targetLanguage, setTargetLanguage] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const fileLabel = file
    ? `${file.name} • ${(file.size / (1024 * 1024)).toFixed(2)} MB`
    : "Drop a file here or browse from your device";

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      setError("Choose a file before starting extraction.");
      return;
    }

    setIsSubmitting(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);
    if (targetLanguage) {
      formData.append("target_lang", targetLanguage);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/process`, {
        method: "POST",
        body: formData,
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || "Unable to process the file.");
      }

      setResult(payload);
    } catch (submissionError) {
      setError(submissionError.message);
      setResult(null);
    } finally {
      setIsSubmitting(false);
    }
  }

  function onDrop(event) {
    event.preventDefault();
    setDragActive(false);

    const droppedFile = event.dataTransfer.files?.[0];
    if (droppedFile) {
      setFile(droppedFile);
      setError("");
    }
  }

  return (
    <div className="app-shell">
      <div className="bg-orb orb-a" />
      <div className="bg-orb orb-b" />

      <header className="hero">
        <p className="eyebrow">Extract. Understand. Structure.</p>
        <h1>Turn scans, screenshots, PDFs, and clips into usable text.</h1>
        <p className="hero-copy">
          Inscriptify pulls text from uploaded files, cleans it up, detects the language,
          and can translate between English and Hindi in the same workflow.
        </p>
      </header>

      <main className="workspace">
        <section className="panel upload-panel">
          <div className="panel-heading">
            <h2>Upload a document</h2>
            <div className="chip-row">
              {supportedTypes.map((type) => (
                <span className="chip" key={type}>
                  {type}
                </span>
              ))}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="upload-form">
            <label
              className={`dropzone ${dragActive ? "active" : ""}`}
              onDragEnter={() => setDragActive(true)}
              onDragOver={(event) => {
                event.preventDefault();
                setDragActive(true);
              }}
              onDragLeave={() => setDragActive(false)}
              onDrop={onDrop}
            >
              <input
                type="file"
                onChange={(event) => {
                  setFile(event.target.files?.[0] || null);
                  setError("");
                }}
                accept=".png,.jpg,.jpeg,.webp,.pdf,.mp4,.avi,.mov"
              />
              <span className="dropzone-title">{file ? "Selected file" : "Drag and drop"}</span>
              <span className="dropzone-copy">{fileLabel}</span>
            </label>

            <div className="controls">
              <label className="field">
                <span>Translation</span>
                <select
                  value={targetLanguage}
                  onChange={(event) => setTargetLanguage(event.target.value)}
                >
                  {languageOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>

              <button type="submit" className="submit-button" disabled={isSubmitting}>
                {isSubmitting ? "Processing..." : "Extract text"}
              </button>
            </div>

            {error ? <p className="error-banner">{error}</p> : null}
          </form>
        </section>

        <section className="panel results-panel">
          <div className="panel-heading">
            <h2>Results</h2>
            <p>Cleaned text, sentence metadata, and translation appear here.</p>
          </div>

          {result ? (
            <div className="result-stack">
              <ResultCard
                title="Extracted text"
                content={result.processed?.clean_text || result.text}
                meta={[
                  `Language: ${result.processed?.language || "unknown"}`,
                  `Intent: ${result.processed?.intent || "unknown"}`,
                  `Sentences: ${result.processed?.sentences?.length || 0}`,
                ]}
              />

              {result.translation ? (
                <ResultCard
                  title="Translation"
                  content={result.translation.translated_text}
                  meta={[
                    `From: ${result.translation.source_lang}`,
                    `To: ${result.translation.target_lang}`,
                    result.translation.metadata?.fallback_used ? "Fallback used" : "Translated",
                  ]}
                />
              ) : null}

              <div className="metrics-grid">
                <Metric
                  label="Original length"
                  value={result.processed?.metadata?.original_length ?? 0}
                />
                <Metric
                  label="Clean length"
                  value={result.processed?.metadata?.clean_length ?? 0}
                />
                <Metric
                  label="Filename"
                  value={result.processed?.metadata?.filename || "Unknown"}
                />
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <p>Upload a file to see extracted text and translation results.</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

function ResultCard({ title, content, meta }) {
  return (
    <article className="result-card">
      <div className="result-header">
        <h3>{title}</h3>
        <div className="chip-row">
          {meta.map((item) => (
            <span className="chip subtle" key={item}>
              {item}
            </span>
          ))}
        </div>
      </div>
      <pre>{content || "No text found."}</pre>
    </article>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default App;
