import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function DocumentViewer({ document, onClose }) {
  return (
    <div className="doc-viewer">
      <span
        className="close-btn"
        onClick={onClose}
      >
        ✕
      </span>

      <h2>{document.title}</h2>

      <p>
        <strong>Source:</strong>{" "}
        {document.source}
      </p>

      <p>
        <strong>Path:</strong>{" "}
        {document.path}
      </p>

      {document.url && (
        <p>
          <strong>Original Source:</strong>{" "}
          <a href={document.url} target="_blank" rel="noreferrer" style={{ color: "#007bff", textDecoration: "underline" }}>
            Open Link
          </a>
        </p>
      )}

      <hr />

      <div className="markdown-body" style={{ overflowX: 'auto', lineHeight: '1.6' }}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {document.content}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default DocumentViewer;