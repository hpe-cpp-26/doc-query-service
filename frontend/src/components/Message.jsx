import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function Message({ message, onCiteClick }) {
  const renderContent = (text) => {
    if (!text) return null;
    if (message.role === "user") return text;

    const processedText = text.replace(/\[(\d+)\](?!\()/g, "[$1](#cite-$1)");

    return (
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ node, href, children, ...props }) => {
            if (href && href.startsWith("#cite-")) {
              const index = parseInt(href.replace("#cite-", ""), 10) - 1;
              const source = message.sources && message.sources[index];
              if (source && onCiteClick) {
                return (
                  <span
                    onClick={(e) => {
                      e.preventDefault();
                      onCiteClick(source);
                    }}
                    style={{
                      color: "#007bff",
                      cursor: "pointer",
                      textDecoration: "underline",
                      fontWeight: "bold",
                    }}
                    title={`View Source ${index + 1}`}
                  >
                    {children}
                  </span>
                );
              }
            }
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                {...props}
              >
                {children}
              </a>
            );
          },
        }}
      >
        {processedText}
      </ReactMarkdown>
    );
  };

  return (
    <div
      className={`message ${message.role === "user" ? "user" : "assistant"}`}
      style={{ lineHeight: "1.5", overflowX: "auto" }}
    >
      {message.role === "user" ? (
        <div style={{ whiteSpace: "pre-wrap" }}>{message.content}</div>
      ) : (
        renderContent(message.content)
      )}
    </div>
  );
}

export default Message;
