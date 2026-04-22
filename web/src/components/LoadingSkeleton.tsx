import React from "react";

export default function LoadingSkeleton() {
  return (
    <div className="assistant-bubble">
      <div style={{ width: "100%" }}>
        <div className="skeleton" style={{ padding: 12 }}>
          <div className="skeleton-line" style={{ width: "60%" }} />
          <div className="skeleton-line" style={{ width: "90%" }} />
          <div className="skeleton-line" style={{ width: "80%" }} />
          <div className="skeleton-line" style={{ width: "50%" }} />
        </div>
      </div>
    </div>
  );
}
