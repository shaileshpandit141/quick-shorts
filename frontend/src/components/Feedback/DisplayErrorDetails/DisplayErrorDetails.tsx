import React from "react";
import "./DisplayErrorDetails.css";

interface Props {
  details: string | string[] | undefined;
}

const DisplayErrorDetails: React.FC<Props> = ({ details }) => {
  if (details === undefined) {
    return null;
  }

  if (typeof details === "string") {
    return (
      <div className="error-details-container">
        <p className="detail">{details}</p>
      </div>
    );
  }

  return (
    <div className="error-details-container">
      {details.map((detail, index) => (
        <p className="detail" key={index}>
          {detail}
        </p>
      ))}
    </div>
  );
};

export default DisplayErrorDetails;
